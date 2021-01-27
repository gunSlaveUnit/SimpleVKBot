#! usr/bin/env python3
# -*- coding: utf8 -*-

from VKBot import VKBot
try:
    import settings
except ImportError:
    exit('Rename settings.py.default.py to settings.py and set ID and TOKEN')

if __name__ == '__main__':
    bot = VKBot(group_id=settings.ID, group_access_key=settings.TOKEN)
    bot.run()
