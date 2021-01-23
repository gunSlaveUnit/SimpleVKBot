#! usr/bin/env python3
# -*- coding: utf8 -*-

from VKBot import VKBot
from key import group_key
from id import group_id

if __name__ == '__main__':
    bot = VKBot(group_id=group_id, group_access_key=group_key)
    bot.run()
