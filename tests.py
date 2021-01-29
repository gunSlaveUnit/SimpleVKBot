#! usr/bin/env python3
# -*- coding: utf8 -*-

from unittest import TestCase
from unittest.mock import patch, Mock, ANY
from unittest import main

from vk_api.bot_longpoll import VkBotMessageEvent

from VKBot import VKBot


class TestBot(TestCase):
    def test_run(self):
        count_call_handle_events = 5
        object_to_pass_to_handle_events = {'a': 1}
        events = [object_to_pass_to_handle_events] * count_call_handle_events
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('VKBot.vk_api.VkApi'):
            with patch('VKBot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = VKBot(group_id='', group_access_key='')
                bot._handle_events = Mock()
                bot.run()

                bot._handle_events.assert_called()
                # TODO: assert below is bad
                # bot._handle_events.assert_any_call(object_to_pass_to_handle_events)
                assert bot._handle_events.call_count == count_call_handle_events

    def test_handle_events(self):
        raw_event_for_test = {
            'type': 'message_new',
            'object': {
                'message': {
                    'date': 1611745974, 'from_id': 223097069,
                    'id': 120, 'out': 0, 'peer_id': 223097069, 'text': 'Ааааа',
                    'conversation_message_id': 118, 'fwd_messages': [], 'important': False,
                    'random_id': 0, 'attachments': [], 'is_hidden': False
                },
                'client_info': {
                    'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link',
                                       'open_photo', 'callback', 'intent_subscribe', 'intent_unsubscribe'],
                    'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 0
                }
            },
            'group_id': 201833632,
            'event_id': 'edd6b907c6b27c817e03bc998c09724c1c8fb1db'
        }

        event = VkBotMessageEvent(raw=raw_event_for_test)
        send_mock = Mock()
        with patch('VKBot.vk_api.VkApi'):
            with patch('VKBot.VkBotLongPoll'):
                bot = VKBot(group_id='', group_access_key='')
                bot._vk_api = Mock()
                bot._vk_api.messages.send = send_mock

                bot._handle_events(event)
                send_mock.assert_called_once_with(
                    user_id=raw_event_for_test['object']['message']['from_id'],
                    message=raw_event_for_test['object']['message']['text'],
                    random_id=ANY
                )


if __name__ == '__main__':
    main()
