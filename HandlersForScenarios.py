#! usr/bin/env python3
# -*- coding: utf8 -*-

import re

RE_NAME_PATTERN = re.compile(r'^[\w\-\s]{3,30}$')
RE_EMAIL_PATTERN = re.compile(r"(\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b)")


def handler_name(text, context):
    """
    The function looks for a name in the text.
    Only the first name encountered.
    :param text: text of message from a user, string
    :param context: dictionary
    :return: bool
    """
    name_matched = re.match(pattern=RE_NAME_PATTERN, string=text)
    if name_matched:
        context['name'] = text
        return True
    else:
        return False


def handler_email(text, context):
    """
    The function looks for all emails in the text.
    :param text: text of message from a user, string
    :param context: dictionary
    :return: bool
    """
    emails_matched = re.findall(pattern=RE_EMAIL_PATTERN, string=text)
    if len(emails_matched) > 0:
        context['email'] = text
        return True
    else:
        return False
