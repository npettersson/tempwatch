#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

tempval = 12.345

obj  = {'tempvalue': tempval}

obj['sensor'] = "28-234234"
obj['date'] = "2016-11-24 11:00:00"

print(json.dumps(obj))