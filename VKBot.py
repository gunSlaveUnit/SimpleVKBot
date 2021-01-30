#! usr/bin/env python3
# -*- coding: utf8 -*-

import logging
from random import randint

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import BotBehaviour
import HandlersForScenarios
import UserState


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
        self._user_states = dict()  # user_id: user_state

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
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info(f' Message of an unprocessed type: {event.type}')
            return
        user_id = event.message['from_id']
        text = event.message['text']
        if user_id in self._user_states:
            text_to_send = self._continue_scenario(user_id, text)
        else:
            # search intent
            for intent in BotBehaviour.INTENTS:
                log.debug(f'User gets {intent}')
                if any(token in text for token in intent['tokens']):
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

    def _continue_scenario(self, user_id, text):
        # continue a scenario
        state = self._user_states[user_id]
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
                self._user_states.pop(user_id)
        else:
            # retry current step
            text_to_send = step['failure_text'].format(**state.context)

        return text_to_send

    def _start_scenario(self, user_id, scenario_name):
        scenario = BotBehaviour.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        self._user_states[user_id] = UserState.UserState(scenario_name, first_step)

        return text_to_send
