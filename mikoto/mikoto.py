# -*- coding: utf-8 -*-

from .markdown import render_markdown


class Mikoto(object):

    def __init__(self, text):
        self.text = text

    @property
    def markdown(self):
        return render_markdown(self.text)
