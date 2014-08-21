# -*- coding: utf-8 -*-

from mikoto.markdown import render_markdown
from mikoto.rst import render_rst
from mikoto.code import render_code

__all__ = ['Mikoto']

class Mikoto(object):

    def __init__(self, text):
        self.text = text

    @property
    def markdown(self):
        return render_markdown(self.text)

    @property
    def restructuredtext(self):
        return render_rst(self.text)

    @property
    def code(self):
        return render_code(self.text)
