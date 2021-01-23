from random import randint

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


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
            print(ex, ex.args)

    def _handle_events(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            self._vk_api.messages.send(user_id=event.message['from_id'],
                                       message=event.message['text'],
                                       random_id=randint(0, VKBot._INFINITE))
