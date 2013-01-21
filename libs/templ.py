#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from jinja2 import (Environment, FileSystemLoader)

class Render():
    """Формирование html-страницы по шаблону jinja"""

    def __init__(self, tpl_folder):
        self.env = Environment()
        self.env.loader = FileSystemLoader(os.path.join(tpl_folder, '.'))

    def render(self, tpl, content):
        tpl = self.env.get_template(tpl)
        return tpl.render(content)