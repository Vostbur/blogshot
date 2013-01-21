#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import json
from codecs import open

def initial(**kwargs):
    """Создание каталогов по данным из конфигурационного файла"""
    def test(param):
        if param in kwargs:
            if not os.path.isdir(kwargs[param]):
                os.makedirs(kwargs[param])
        else:
            print("Can't find '%s' in config file." % param)
            sys.exit(1)
    for folder in ['source', 'draft', 'output', 'nav_pages']:
        test(folder)
    save('dump.db', '{}')

def load_config(path=os.getcwd(), fname='config.json'):
    """Загрузка конфигурации из файла формата json
       By default './config.json'"""
    config = os.path.join(path, fname)
    if not os.path.isfile(config):
        print("Can't find", fname)
        sys.exit(1)
    return json.load(open(config))

def clear(dname, ext='.html'):
    """Удаление всех файлов с расширением ext из каталога dname"""
    for the_file in os.listdir(dname):
        if the_file.endswith(ext):
            file_path = os.path.join(dname, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print(e)

def files(dname, ext='.md'):
    """Получение списка файлов с расширением ext из каталога dname"""
    files_list = []
    for the_file in os.listdir(dname):
        if the_file.endswith('.md'):
            files_list.append(os.path.join(dname, the_file))
    return files_list

def save(fname, content):
    with open(fname, encoding='utf-8', mode='w') as f:
        f.write(content)

def server(dname, port = 8000):
    try:
        import SimpleHTTPServer as srvmod
    except ImportError:
        import http.server as srvmod
    try:
        import SocketServer as socketserver
    except ImportError:
        import socketserver
    os.chdir(dname)
    Handler = srvmod.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    print("serving at port", port)
    httpd.serve_forever()

def usage():
    print("""Simple Static Pages Generator

Usage: python shot.py {-h,--help | -i,--init | -r,--regen | -d,--draft | -s,--server}

  -h, --help\tThis help
  -i, --init\tInitial setup.
  -r, --regen\tRegen all files.
  -d, --draft\tRegen from draft.
  -s, --server\tStart internal server.

Testing for python-2.7.3 on Windows
(c) Copyright 2013, Alexey Rubtsov""")
    sys.exit(1)