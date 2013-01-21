#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from markdown import Markdown
from codecs import open

class Convert:
    """Ковертирование из markdown в html и получение заголовка статьи"""

    def __init__(self):
        self._md = Markdown(extensions = ['extra', 'meta', 'codehilite', 'nl2br'])

    def read(self):
        return open(self.fname, encoding="utf-8").read()
    
    def test(self, pattern, tag):
        return re.match(pattern, tag)
        
    def go(self, fname):
        self.fname = fname
        content = self._md.convert(self.read())
        meta = self._md.Meta

        test = [None for i in ['date', 'title', 'slug'] if i not in meta.keys()]
        if None in test:
            return None
        if self.test(r'^\d{4}-\d{2}-\d{2}$', meta['date'][0])\
            and self.test(r'^[a-zA-Z0-9-]+$', meta['slug'][0]):
                return {'date': meta['date'][0], 
                        'title': meta['title'][0],
                        'slug': meta['slug'][0],
                        'content': content}
        else:
            return None