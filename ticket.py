# !usr/bin/env python3
# -*- coding: utf-8 -*-

import io

from PIL import Image, ImageDraw, ImageFont

TEMPLATE_PATH = 'ticket_template.png'
FONT_PATH = 'Roboto-Regular.ttf'
FONT_SIZE = 20

BLACK_COLOR_FONT = (0, 0, 0, 255)

NAME_OFFSET = (245, 260)
EMAIL_OFFSET = (245, 310)


def generate_ticket(user_name='DefaultName', user_email='DefaultEmail'):
    template_ticket = Image.open(TEMPLATE_PATH).convert('RGBA')
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    draw = ImageDraw.Draw(template_ticket)
    draw.text(NAME_OFFSET, user_name, font=font, fill=BLACK_COLOR_FONT)
    draw.text(EMAIL_OFFSET, user_email, font=font, fill=BLACK_COLOR_FONT)

    temp_file = io.BytesIO()
    template_ticket.save(temp_file, 'png')
    temp_file.seek(0)

    return temp_file
