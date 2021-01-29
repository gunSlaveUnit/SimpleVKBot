#! usr/bin/env python3
# -*- coding: utf8 -*-

INTENTS = [
    {
        'name': 'Дата проведения',
        'tokens': ('когда', 'во сколько', 'дата', 'дату'),
        'scenario': None,
        'answer': 'Мероприятие проводится 30 января, регистрация начнётся в 12:00'
    },
    {
        'name': 'Место проведения',
        'tokens': ('где', 'место', 'локация', 'адрес'),
        'scenario': None,
        'answer': 'Мероприятие будет проводится в ИГЭУ им. Ленина, актовый зал, 4 этаж'
    },
    {
        'name': 'Регистрация',
        'tokens': ('регист', 'добав'),
        'scenario': 'registration',
        'answer': None
    }
]

SCENARIOS = {
    'registration': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Для регистрации введите Ваше имя. Оно будет на Вашем бейджике.',
                'failure_text': 'Имя должно состоять из 3-30 букв и содержать пробел.',
                'handler': 'handler_name',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Введите Ваш email. На него мы отправим билет.',
                'failure_text': 'Введенный email некорректен, попробуйте ещё раз.',
                'handler': 'handler_email',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Благодарим Вас за регистрацию, {name}! Мы отправили билет на Ваш email,'
                        'распечатайте его',
                'failure_text': None,
                'handler': None,
                'next_step': None
            },
        }
    }
}

DEFAULT_ANSWER = 'Я не знаю, как на это ответить. ' \
                 'Я могу ответить про дату, место проведения мероприятия,' \
                 'а также зарегистрировать Вас.'
