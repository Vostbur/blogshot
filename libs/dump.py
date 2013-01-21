#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from codecs import open

class Dump():
    def __init__(self, filename=None):
        self.filename = filename if filename else 'dump.db'
        if os.path.isfile(self.filename):
            self.archive = self.load(self.filename)

    def load(self, fd):
        try:
            return json.load(open(fd, 'r'))
        except Exception:
            pass

    def sync(self):
        with open(self.filename, encoding='utf-8', mode='w') as fl:
            json.dump(self.archive, fl, ensure_ascii=False, indent=True)

    def __repr__(self):
        return '\n'.join([x for x in self.archive.keys()])
