#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import os, getopt
import sys
from shutil import move, copyfile
from collections import OrderedDict
from pyatom import AtomFeed
from datetime import datetime

from libs.tools import *
from libs.mdown import Convert
from libs.templ import Render
from libs.dump import Dump

config = load_config()
md = Convert()
tpl = Render(config['templates']['folder'])

def work(the_file, dmp = None):
    result = md.go(the_file)
    if result == None:
        print("File %s has wrong head." % the_file)
        return None
    else:
        result['site'] = config['site']
        result['author'] = config['author']
        result['feed'] = config['feed']
        result['disqus'] = config['disqus']
        content = tpl.render(config['templates']['article'], result)
        if dmp != None:
            save(os.path.join(config['output'], result['date'] + '.html'), content)
            dmp.archive[result['date'] + '.html'] = result
        return content

def archive_page(dmp):
    result = {}
    result['site'] = config['site']
    result['author'] = config['author']
    result['feed'] = config['feed']
    result['disqus'] = config['disqus']
    result['content'] = OrderedDict(sorted(dmp.archive.items(), reverse=True))
    content = tpl.render(config['templates']['archive'], result)
    save(os.path.join(config['output'], 'archive.html'), content)
    idx = os.path.join(config['output'], result['content'].items()[0][0])
    copyfile(idx, os.path.join(config['output'], 'index.html'))

def static_page():
    flist = files(config['nav_pages'])
    for the_file in flist:
        content = work(the_file)
        if content:
            save(os.path.join(config['output'],\
                os.path.basename(the_file)[:-3] + '.html'), content)

def rss(dmp):
    url = config['site'][:-1] if config['site'].endswith('/') else config['site']
    feed = AtomFeed(title=config['title'],
                feed_url=url + "/feed",
                url=url,
                author=config['author'])
    feed_dict = OrderedDict(sorted(dmp.archive.items(), reverse=True))
    #current_date = datetime.now().strftime('%Y-%m-%d')
    try:
        for x in xrange(10):
            feed.add(title=feed_dict.items()[x][1]['title'],
                    content=feed_dict.items()[x][1]['content'],
                    content_type="html",
                    author=config['author'],
                    url=url + feed_dict.items()[x][0],
                    updated=datetime.strptime(feed_dict.items()[x][1]['date'], '%Y-%m-%d')
                    )
    except IndexError:
        pass
    save(os.path.join(config['output'], config['feed']), feed.to_string())

def regen_mode(): # режим полной перегенирации файлов
    clear(config['output'])
    save('dump.db', '{}')
    dmp = Dump()
    flist = files(config['source'])
    for the_file in flist:
        work(the_file, dmp)
    archive_page(dmp)
    rss(dmp)
    dmp.sync()
    static_page()

def draft_mode(): # Режим генерации из черновиков
    dmp = Dump()
    flist = files(config['draft'])
    for the_file in flist:
        if work(the_file, dmp):
            move(the_file, config['source'])
    archive_page(dmp)
    rss(dmp)
    dmp.sync()

def main(args):
    try:
        if not args:
            raise getopt.GetoptError('Error')
        opt, arg = getopt.getopt(args, 'hirds', ['help', 'init', 'regen', 'draft', 'server'])
    except getopt.GetoptError, e:
        usage()
    if arg:
        usage()
    for o, a in opt:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-i', '--init'):
            initial(**config)
        elif o in ('-r', '--regen'):
            regen_mode()
        elif o in ('-d', '--draft'):
            draft_mode()
        elif o in ('-s', '--server'):
            server(config['output'], config['port'])
        else:
            usage()

if __name__ == '__main__':
    main(sys.argv[1:])
