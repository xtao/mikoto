# -*- coding: utf-8 -*-

from pygments import highlight
from pygments.lexers import TextLexer
from pygments.formatters import HtmlFormatter


def render_code(text):
    lexer = TextLexer(encoding='utf-8')
    return highlight(src,
                     lexer,
                     HtmlFormatter(linenos=True,
                                   lineanchors='L',
                                   anchorlinenos=True,
                                   encoding='utf-8'))
