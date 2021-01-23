from random import randint
import logging

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

log = logging.getLogger('bot')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s '
                                              '%(levelname)s'
                                              '%(message)s'))
log.addHandler(stream_handler)
log.setLevel(logging.DEBUG)
stream_handler.setLevel(logging.DEBUG)


class VKBot:
    _INFINITE = 2**32

    def __init__(self, group_id=None, group_access_key=None):
        self._id = group_id
        self._token = group_access_key

        self._vk = vk_api.VkApi(token=self._token)
        self._vk_api = self._vk.get_api()
        self._vk_longpoller = VkBotLongPoll(vk=self._vk, group_id=self._id)

    def run(self):
        try:
            for event in self._vk_longpoller.listen():
                self._handle_events(event=event)
        # TODO: write exceptions
        except Exception as ex:
            log.debug(f'Error in event handling: {ex} - {ex.args}')

    def _handle_events(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            self._vk_api.messages.send(user_id=event.message['from_id'],
                                       message=event.message['text'],
                                       random_id=randint(0, VKBot._INFINITE))

            log.debug(f' Message: {event.message["text"]}')
        else:
            # log.debug(f'Message of an unprocessed type: {event.type}')
            log.debug(f' Message of an unprocessed type: {event.type}')
