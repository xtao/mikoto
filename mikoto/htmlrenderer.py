# -*- coding: utf-8 -*-

import re
from cgi import escape
import misaka
from pygments.lexers import get_lexer_by_name
from mikoto.libs.emoji import parse_emoji


class HtmlRenderer(misaka.HtmlRenderer):

    def postprocess(self, text):
        if not text:
            return text
        text = render_checklist(text)
        text = parse_emoji(text, is_escape=False)
        return RE_USER_MENTION.sub(USER_LINK_TEXT, text)

    def block_code(self, text, lang):
        if not lang:
            text = escape(text.strip())
            text = self.__text_to_unichr(text)
            return '\n<pre><code>%s</code></pre>\n' % text
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

    def codespan(self, text):
        text = self.__text_to_unichr(text)
        return '<code>%s</code>' % text

    def header(self, text, level):
        if level == 1 and re.match(r'\d+', text):
            return '#' + text
        return '<h%s>%s</h%s>' % (level, text, level)

    def __text_to_unichr(self, text):
        text = text.replace("@", "&#64;")
        return text

    def __link_to_local_project(self, link):
        if not (link.startswith("http://")
                or link.startswith("https://")):
            link = "[PROJECT]%s" % link
        return link

    def image(self, link, title, alt_text):
        alt_text = alt_text or ""
        link = self.__link_to_local_project(link)
        return '<img src="%s" alt="%s">' % (link, alt_text)

    def link(self, link, title, content):
        title = title or ""
        link = self.__link_to_local_project(link)
        return '<a href="%s" title="%s">%s</a>' % (link, title, content)


def render_checklist(content):
    i = 0
    while 1:
        m = re.search(RE_CHECKBOX_IN_HTML, content)
        if not m:
            break
        t = m.group(0).replace('<li>', '').replace('</li>', '')
        source = '<li><label><input type="checkbox" data-item-index="%d"' % i
        end = lambda type, idx: '> ' + t.lstrip(type).strip() + \
              '</label></li>' + content[idx + len(t) + len('<li></li>'):]

        if t.startswith(CHECKED):
            checked_idx = content.find(HTML_CHECKED)
            content = content[:checked_idx] + source + ' checked' + \
                      end(CHECKED, checked_idx)
        else:
            unchecked_idx = content.find(HTML_UNCHECKED)
            content = content[:unchecked_idx] + source + \
                      end(UNCHECKED, unchecked_idx)
        i += 1
    return content
