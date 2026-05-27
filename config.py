#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_ID    = int(os.environ.get("API_ID", 0))
    API_HASH  = os.environ.get("API_HASH", "")
    AUTH_USERS = os.environ.get("AUTH_USERS", "6824252172")
    MONGO_URI  = os.environ.get("MONGO_DB_URI", "")
