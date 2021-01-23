#! usr/bin/env python3
# -*- coding: utf8 -*-

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from key import group_key
from id import group_id


class VKBot:
    def __init__(self, group_id=None, group_access_key=None):
        self._id = group_id
        self._token = group_access_key

    def run(self):
        pass


if __name__ == '__main__':
    bot = VKBot(group_id=group_id, group_access_key=group_key)
    bot.run()
