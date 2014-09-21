# -*- coding: utf-8 -*-

import os
import re

EMOJIS = [
    ':airplane:', ':alien:', ':art:', ':bear:', ':beer:', ':bike:', ':bomb:',
    ':book:', ':bulb:', ':bus:', ':cake:', ':calling:', ':clap:', ':cocktail:',
    ':code:', ':computer:', ':cool:', ':cop:', ':email:', ':feet:', ':fire:',
    ':fish:', ':fist:', ':gift:', ':hammer:', ':heart:', ':iphone:', ':key:',
    ':leaves:', ':lgtm:', ':lipstick:', ':lock:', ':mag:', ':mega:', ':memo:',
    ':moneybag:', ':new:', ':octocat:', ':ok:', ':palm_tree:', ':pencil:',
    ':punch:', ':runner:', ':scissors:', ':ship:', ':shipit:', ':ski:', ':smile:',
    ':smoking:', ':sparkles:', ':star:', ':sunny:', ':taxi:', ':thumbsdown:',
    ':thumbsup:', ':tm:', ':tophat:', ':train:', ':trollface:', ':v:', ':vs:',
    ':warning:', ':wheelchair:', ':zap:', ':zzz:', ':see_no_evil:', ':pig:',
    ':hear_no_evil:', ':speak_no_evil:', ':monkey:', ':monkey_face:', ':beers:',
    ':ruby:',
]


GROUPED_EMOJIS = {
    ":mergetime:": """
:zap::zap::zap::zap::zap::zap::zap::zap::zap::zap:
:zap::metal: M E R G E T I M E :metal::zap:
:zap::zap::zap::zap::zap::zap::zap::zap::zap::zap:
""",
    ":sparklock:": """
:black_circle::point_down::black_circle:
:point_right::sparkler::point_left:
:black_circle::point_up_2::black_circle:
""",
    ":myballoon:": """
:cloud::partly_sunny::cloud::cloud::cloud::cloud::cloud:

        :balloon:

                    :runner::dash:
""",
    ":getit:": """
:balloon:
  :raised_hand:
""",
    ":apollo:": """
:octocat:      :star2:             :us:
:sparkles:                :sparkles:   :full_moon:
:star2:     :dizzy:         :rocket:
        :sparkles:     :collision:
:partly_sunny:        :collision:       :sparkles:
:zap:   :collision:
:earth_asia:          :sparkles:         :dizzy:
""",
}


class Emoji(object):

    def __init__(self, emojis=None, grouped_emojis=None):
        self.emojis = emojis or []
        self.grouped_emojis = grouped_emojis or {}

    def init(self):
        self.emoji_pattern = re.compile(r'(' + '|'.join([re.escape(x) for x in self.emojis]) + r')')
        self.emoji_only_pattern = re.compile(r'^<p>\s*(' + '|'.join([re.escape(x) for x in self.emojis]) + r')\s*</p>$')
        self.grouped_emoji_pattern = re.compile('|'.join([re.escape(x) for x in self.grouped_emojis.keys()]))


emoji = Emoji(emojis=EMOJIS, grouped_emojis=GROUPED_EMOJIS)
emoji.init()


def render_emoji(text):
    if not text:
        return ''
    text = render_grouped_emoji(emoji, text)
    if emoji.emoji_only_pattern.match(text.strip()):
        emoji_img = '<img src="/static/emoji/%s.png" align="absmiddle"/>'
    else:
        emoji_img = '<img src="/static/emoji/%s.png" height="20" width="20" align="absmiddle"/>'
    text = emoji.emoji_pattern.sub(lambda x: emoji_img % x.group().strip(':'), text)
    return text


def render_grouped_emoji(text):
    groups = set(emoji.grouped_emoji_pattern.findall(text))
    for group in groups:
        group_text = emoji.grouped_emojis[group]
        group_text = group_text.replace(' ', '&nbsp;')
        group_text = group_text.replace('\n', "<br/>")
        text = text.replace(group, group_text)
    return text


def discover_emoji():
    sub_emoji = 'hub/static/emoji'
    emoji_file_path = os.path.join(os.path.curdir, sub_emoji)
    realpath = os.path.dirname(os.path.realpath(__file__))
    cur_path = os.path.join(realpath, os.path.pardir, sub_emoji)
    for dir in [emoji_file_path, cur_path]:
        abs_emoji_dir = os.path.abspath(dir)
        if os.path.isdir(abs_emoji_dir):
            files = os.listdir(abs_emoji_dir)
            if files:
                return [':{}:'.format(fn[:-4]) for fn in files
                        if fn.endswith('.png')]
    return EMOJIS
