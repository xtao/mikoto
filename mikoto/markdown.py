# -*- coding: utf-8 -*-

import misaka
from mikoto.htmlrenderer import HtmlRenderer

_generic_renderer = HtmlRenderer(misaka.HTML_HARD_WRAP |
                                 misaka.HTML_SAFELINK |
                                 misaka.HTML_SKIP_STYLE |
                                 misaka.HTML_SKIP_SCRIPT |
                                 misaka.HTML_ESCAPE)

_markdown_renderer = misaka.Markdown(_generic_renderer,
                                     extensions=misaka.EXT_FENCED_CODE |
                                     misaka.EXT_NO_INTRA_EMPHASIS |
                                     misaka.EXT_AUTOLINK |
                                     misaka.EXT_TABLES |
                                     misaka.EXT_STRIKETHROUGH)


def render_markdown(content):
    if not content:
        content = ''
    return _markdown_renderer.render(content)
