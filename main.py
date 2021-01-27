#! usr/bin/env python3
# -*- coding: utf8 -*-

from VKBot import VKBot
import settings

if __name__ == '__main__':
    bot = VKBot(group_id=settings.group_id, group_access_key=settings.group_key)
    bot.run()
