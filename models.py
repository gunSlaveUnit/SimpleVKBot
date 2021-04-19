#! usr/bin/env python3
# -*- coding: utf8 -*-
from pony.orm import Database, Required, Json

import settings

db = Database()
db.bind(**settings.DB_CONFIG)


class UserState(db.Entity):
    """User state in scenario"""
    user_id = Required(str, unique=True)
    scenario = Required(str)
    step = Required(str)
    context = Required(Json)


class Registration(db.Entity):
    name = Required(str)
    email = Required(str)


db.generate_mapping(create_tables=True)
