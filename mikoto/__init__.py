# -*- coding: utf-8 -*-

from mikoto.markdown import render_markdown, init_markdown
from mikoto.rst import render_rst
from mikoto.code import render_code, render_highlight_code
from mikoto.text import translate_to_unicode

__all__ = ['Mikoto']


class Mikoto(object):

    def __init__(self):
        self.markdown = None

    def init_markdown(self, **kw):
        self.markdown = init_markdown(**kw)

    def render_markdown(self, text, path):
        text = translate_to_unicode(text)
        if self.markdown:
            return render_markdown(text)
        return self.markdown.render(text)

    def render_restructuredtext(self, text, path):
        text = translate_to_unicode(text)
        return render_rst(text)

    def render_code(self, text, path):
        text = translate_to_unicode(text)
        return render_code(text)

    def render_highlight_code(self, text, path):
        text = translate_to_unicode(text)
        return render_highlight_code(text, path)
