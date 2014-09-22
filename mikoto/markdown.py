# -*- coding: utf-8 -*-

import misaka
from mikoto.htmlrenderer import HtmlRenderer

_render_flags = misaka.HTML_HARD_WRAP \
    | misaka.HTML_SAFELINK \
    | misaka.HTML_SKIP_STYLE \
    | misaka.HTML_ESCAPE

if hasattr(misaka, 'HTML_SKIP_SCRIPT'):
    _render_flags |= misaka.HTML_SKIP_SCRIPT

_generic_renderer = HtmlRenderer(_render_flags)

_markdown_renderer = misaka.Markdown(_generic_renderer,
                                     extensions=misaka.EXT_FENCED_CODE |
                                     misaka.EXT_NO_INTRA_EMPHASIS |
                                     misaka.EXT_AUTOLINK |
                                     misaka.EXT_TABLES |
                                     misaka.EXT_STRIKETHROUGH)


def render_markdown(text):
    if not text:
        text = ''
    renderer = _markdown_renderer
    return renderer.render(text)

def init_markdown(emoji=None, link_prefix=None):
    html = HtmlRenderer(_render_flags, emoji=emoji, link_prefix=link_prefix)
    markdown = misaka.Markdown(html,
                               extensions=misaka.EXT_FENCED_CODE |
                               misaka.EXT_NO_INTRA_EMPHASIS |
                               misaka.EXT_AUTOLINK |
                               misaka.EXT_TABLES |
                               misaka.EXT_STRIKETHROUGH)
    return markdown
