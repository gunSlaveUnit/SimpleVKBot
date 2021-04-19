#! usr/bin/env python3
# -*- coding: utf8 -*-

import logging
from random import randint

import vk_api
from pony.orm import db_session
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import BotBehaviour
import HandlersForScenarios
import models


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

    @db_session
    def _handle_events(self, event):
        """
        Processing an event depending on its type
        :param event: VkBotMessageEvent object
        :return: None
        """
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info(f' Message of an unprocessed type: {event.type}')
            return
        user_id = event.message['from_id']
        text = event.message['text']

        state = models.UserState.get(user_id=str(user_id))

        if state is not None:
            text_to_send = self._continue_scenario(text, state)
        else:
            # search intent
            for intent in BotBehaviour.INTENTS:
                log.debug(f'User gets {intent}')
                if any(token in text.lower() for token in intent['tokens']):
                    # run intent
                    if intent['answer']:
                        text_to_send = intent['answer']
                    else:
                        text_to_send = self._start_scenario(user_id, intent['scenario'])
                    break
                else:
                    text_to_send = BotBehaviour.DEFAULT_ANSWER

        self._vk_api.messages.send(
            user_id=user_id,
            message=text_to_send,
            random_id=randint(0, VKBot._INFINITE_TO_GENERATE_UNIQUE_MESSAGE_NUMBER)
        )

    def _start_scenario(self, user_id, scenario_name):
        scenario = BotBehaviour.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        models.UserState(user_id=str(user_id), scenario=scenario_name, step=first_step, context={})

        return text_to_send

    def _continue_scenario(self, text, state):
        steps = BotBehaviour.SCENARIOS[state.scenario]['steps']
        step = steps[state.step]
        handler = getattr(HandlersForScenarios, step['handler'])
        if handler(text=text, context=state.context):
            # next step
            next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**state.context)
            if next_step['next_step']:
                # switch to next step
                state.step = step['next_step']
            else:
                # finish scenario
                log.info('Registered: {name} {email}'.format(**state.context))
                models.Registration(name=state.context['name'], email=state.context['email'])
                state.delete()
        else:
            # retry current step
            text_to_send = step['failure_text'].format(**state.context)

        return text_to_send
