#! usr/bin/env python3
# -*- coding: utf8 -*-

class UserState:
    """
    User state within a script.
    """
    def __init__(self, scenario, step, context=None):
        self.scenario = scenario
        self.step = step
        self.context = context or {}
