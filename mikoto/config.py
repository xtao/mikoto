# -*- coding: utf-8 -*-

from mikoto.markdown import generate_markdown_renderer


class Config(object):

    def __init__(self, emoji):
        self.emoji = emoji
        self.markdown_renderer = generate_markdown_renderer(emoji)

