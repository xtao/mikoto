# -*- coding: utf-8 -*-

from __future__ import absolute_import
import re
import chardet

from pygments.formatters import HtmlFormatter
from pygments.lexers import (TextLexer,
                             guess_lexer_for_filename,
                             MakoHtmlLexer,
                             PythonLexer,
                             RstLexer)
from pygments.util import ClassNotFound
from pygments import highlight

from mikoto.markdown import render_markdown
from mikoto.libs.consts import (SOURCE_FILE, NOT_GENERATED,
                                IGNORE_FILE_EXTS, IS_GENERATED)
from mikoto.libs.emoji import parse_emoji


RST_RE = re.compile(r'.*\.re?st(\.txt)?$')
RE_TICKET = re.compile(r'(?:^|\s)#(\d+)')
RE_ISSUE = re.compile(r'(?:^|\s)#issue(\d+)')
RE_USER_MENTION = re.compile(r'(^|\W)@([a-zA-Z0-9_]+)')
RE_COMMIT = re.compile(r'(^|\s)([0-9a-f]{7,40})')
RE_IMAGE_FILENAME = re.compile(
    r'^.+\.(?:jpg|png|gif|jpeg|mobileprovision|svg|ico)$', flags=re.IGNORECASE)
RE_CHECKBOX_IN_HTML = re.compile('<li>\[[x\s]\].+</li>')
RE_CHECKBOX_IN_TEXT = re.compile('- (\[[x\s]\]).+')

CHECKED = '[x]'
UNCHECKED = '[ ]'
HTML_CHECKED = '<li>[x]'
HTML_UNCHECKED = '<li>[ ]'
RE_PR_IN_MESSAGE = re.compile(r'(?:^|\s)#(\d+)(?:\s|$)')
RE_ISSUE_IN_MESSAGE = re.compile(r'(?:^|\s)#issue(\d+)(?:\s|$)')

TICKET_LINK_TEXT = r'<a href="/%s/pull/\1/" class="issue-link">#\1</a>'
ISSUE_LINK_TEXT = r'<a href="/%s/issues/\1/" class="issue-link">#\1</a>'
COMMIT_LINK_TEXT = r' <a href="/%s/commit/\2">\2</a>'
USER_LINK_TEXT = r'\1<a href="/people/\2/" class="user-mention">@\2</a>'


class _CodeHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_div(self._wrap_pre(self._wrap_a_line(source)))

    def _wrap_a_line(self, source):
        for i, t in source:
            if i == 1:
                # it's a line of formatted code
                t = '<div>' + t + '</div>'
            yield i, t


def decode_charset_to_unicode(charset, default='utf-8'):
    try:
        return charset.decode(default)
    except UnicodeDecodeError:
        charset_encoding = chardet.detect(charset).get('encoding') or default
        return charset.decode(charset_encoding, 'ignore')


def highlight_code(path, src, div=False, **kwargs):
    src = decode_charset_to_unicode(src)
    try:
        if path.endswith(('.html', '.mako')):
            lexer = MakoHtmlLexer(encoding='utf-8')
        elif path.endswith('.ptl'):
            lexer = PythonLexer(encoding='utf-8')
        elif path.endswith('.md'):
            lexer = RstLexer(encoding='utf-8')
        else:
            if path.endswith(IGNORE_FILE_EXTS):
                src = 'Hmm.., this is binary file.'
            lexer = guess_lexer_for_filename(path, src)
        lexer.encoding = 'utf-8'
        lexer.stripnl = False
    except ClassNotFound:
        # no code highlight
        lexer = TextLexer(encoding='utf-8')
    if div:
        formatter = _CodeHtmlFormatter
    else:
        formatter = HtmlFormatter

    src = highlight(src, lexer, formatter(linenos=True,
                                          lineanchors='L',
                                          anchorlinenos=True,
                                          encoding='utf-8',
                                          **kwargs))
    return src


def get_checkbox_count(content):
    m = re.findall(RE_CHECKBOX_IN_TEXT, content)
    if m:
        checked = filter(lambda x: x == CHECKED, m)
        return (len(checked), len(m))


def is_binary(fname):
    ext = fname.split('.')
    if ext is None:
        return False
    if len(ext) == 1:
        return ext[0] not in SOURCE_FILE
    ext = '.' + ext[-1]
    if ext in IS_GENERATED:
        return False
    if ext in IGNORE_FILE_EXTS or ext not in (SOURCE_FILE + NOT_GENERATED):
        return True
    return False


def get_mentions_from_text(text):
    try:
        from models.team import Team
    except ImportError:
        from mikoto.libs.mock import Team
    recipients = RE_USER_MENTION.findall(text)
    users = set()
    for _, r in recipients:
        t = Team.get_by_uid(r)
        if t:
            users.update(t.all_members)
        else:
            users.add(r)
    return list(users)


# TODO: move out, not recommended
def render_markdown_with_team(content, team):
    text = render_markdown(content)
    text = re.sub(RE_TICKET, r'<a href="' + team.url +
                  r'issues/\1/" class="issue-link">#\1</a>', text)
    return parse_emoji(text, is_escape=False)


def render_commit_message(message, project):
    text = parse_emoji(message)
    text = re.sub(RE_PR_IN_MESSAGE,
                  r' <a href="/%s/newpull/\1">#\1</a> ' % project.name,
                  text)
    text = re.sub(RE_ISSUE_IN_MESSAGE,
                  r' <a href="/%s/issues/\1">#\1</a> ' % project.name,
                  text)
    text = text.decode('utf8')
    return text


def render_markdown_with_project(content, project_name):
    text = render_markdown(content)
    text = re.sub(RE_TICKET,
                  TICKET_LINK_TEXT % project_name,
                  text)
    text = re.sub(RE_ISSUE,
                  ISSUE_LINK_TEXT % project_name,
                  text)
    text = re.sub(RE_COMMIT,
                  COMMIT_LINK_TEXT % project_name,
                  text)
    text = text.replace("[PROJECT]", "/%s/raw/master/" % project_name)
    return text


def render(content, project_name=None):
    if project_name:
        return render_markdown_with_project(content, project_name)
    return render_markdown(content)
