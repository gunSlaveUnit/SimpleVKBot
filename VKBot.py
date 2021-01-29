#! usr/bin/env python3
# -*- coding: utf8 -*-

from random import randint
import logging

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def configure_logging():
    global log
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    stream_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename='bot.log', mode='a', encoding='utf8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    file_handler.setLevel(logging.DEBUG)

    log = logging.getLogger('bot')
    log.setLevel(logging.DEBUG)
    log.addHandler(stream_handler)
    log.addHandler(file_handler)


class VKBot:
    """
    Registration Bot for conference.
    For vk.com.

    Bot supports questions about date, place and scenario of registration:
    - Ask name
    - Ask email
    - Say about successful registration.
    If the step is not complete, ask a clarifying question.

    Use Python 3.9.0
    Use vk_api 11.9.1
    """
    _INFINITE_TO_GENERATE_UNIQUE_MESSAGE_NUMBER = 2 ** 32

    def __init__(self, group_id=None, group_access_key=None):
        """
        :param group_id: community id from vk.com
        :param group_access_key: unique secret token to access your community
        """
        self._id = group_id
        self._token = group_access_key

        self._vk = vk_api.VkApi(token=self._token)
        self._vk_api = self._vk.get_api()
        self._vk_longpoller = VkBotLongPoll(vk=self._vk, group_id=self._id)

        configure_logging()

    def run(self):
        """
        Bot launch
        :return: None
        """
        try:
            for event in self._vk_longpoller.listen():
                self._handle_events(event=event)
        # TODO: write exceptions
        except Exception as ex:
            log.exception(f'Error in event handling: {ex} - {ex.args}')

    def _handle_events(self, event):
        """
        Processing an event depending on its type
        :param event: VkBotMessageEvent object
        :return: None
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            self._vk_api.messages.send(
                user_id=event.message['from_id'],
                message=event.message['text'],
                random_id=randint(0, VKBot._INFINITE_TO_GENERATE_UNIQUE_MESSAGE_NUMBER)
            )

            log.debug(f' Message: {event.message["text"]}')
        else:
            # log.debug(f'Message of an unprocessed type: {event.type}')
            log.info(f' Message of an unprocessed type: {event.type}')
