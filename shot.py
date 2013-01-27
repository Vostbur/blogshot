#!/usr/bin/env python
# coding: utf-8

import os
import sys
import json
import getopt
from glob import glob
from codecs import open
from pyatom import AtomFeed
from markdown import Markdown
from datetime import datetime
from shutil import move, copyfile
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader

class SelfSyncedDict(dict):
    '''Dict is saved to file inside with-statement'''
    def __init__(self, fname, *args, **kwargs):
        self.fname = fname
        if os.path.isfile(fname):
            self.update(self.load())
        super(SelfSyncedDict, self).__init__(*args, **kwargs)

    def load(self):
        return json.load(open(self.fname, encoding='utf-8'))

    def __enter__(self):
        return self

    def __exit__(self, *exit_params):
        json.dump(self, open(self.fname, encoding='utf-8', mode='w'), ensure_ascii=False, indent=4)

class Entry:
    '''Markdown to HTML'''
    def __init__(self):
        self._md = Markdown(extensions = ['extra', 'meta', 'codehilite', 'nl2br'])
        
    def convert(self, fname):
        content = self._md.convert(open(fname, encoding="utf-8").read())
        meta = self._md.Meta

        if set(meta.keys()) == set(['date', 'title', 'slug']):
            return {meta['date'][0]:{
                                        'title': meta['title'][0], 'slug': meta['slug'][0], 'content': content
                                    }
                    }

class Post:
    '''Render HTML to jinja2 template'''
    def __init__(self, tpl_folder):
        self.env = Environment()
        self.env.loader = FileSystemLoader(os.path.join(tpl_folder, '.'))

    def render(self, tpl, content):
        return self.env.get_template(tpl).render(content)

def load_config(fname, path=os.getcwd()):
    config = os.path.join(path, fname)
    if not os.path.isfile(config):
        print("Can't find", fname)
        sys.exit(1)
    return json.load(open(config, encoding='utf-8'))

def save(fname, content):
    with open(fname, encoding='utf-8', mode='w') as f:
        f.write(content)

def rss(index):
    url = config['site'][:-1] if config['site'].endswith('/') else config['site']
    feed = AtomFeed(title=config['title'],
                feed_url=url + "/feed",
                url=url,
                author=config['author'])
    for k, v in index.iteritems():
        feed.add(title=v['title'],
                content=v['content'],
                content_type="html",
                author=config['author'],
                url=url + k + '.html',
                updated=datetime.strptime(k, '%Y-%m-%d')
                )
    save(os.path.join(config['output'], config['feed']), feed.to_string())

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

Usage: python shot.py {-h,--help | -n,--new | -r,--regen | -s,--server}

  -h, --help    This help.
  -n, --new     New entry.
  -r, --regen   Regen all files.
  -s, --server  Start internal server.

(c) 2013, Alexey Rubtsov""")
    sys.exit(1)

def new_entry():
    pattern = 'date: %(field)s\ntitle: %(field)s\nslug: %(field)s\n\n%(field)s\n======' % {'field': current_date}
    fname = os.path.join(config['source'], current_date + '.md')
    save(fname, pattern)
    os.system(config['editor'] % fname)

def static_page():
    for f in glob(config['nav_pages'] + '/*.md'):
        page = entry.convert(f)
        save(os.path.join(config['output'], os.path.basename(f)[:-3] + '.html'),
             post.render(config['templates']['article'], 
                dict(config, **page.popitem()[1])))

def initial():
    def test(param):
        if param in config:
            if not os.path.isdir(config[param]):
                os.makedirs(config[param])
        else:
            print("Can't find '%s' in config file." % param)
            sys.exit(1)
    for folder in ['source', 'output', 'nav_pages']:
        test(folder)

def clear(dname, ext='.html'):
    for the_file in os.listdir(dname):
        if the_file.endswith(ext):
            file_path = os.path.join(dname, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print(e)

def regen():
    initial()
    clear(config['output'])
    if os.path.isfile('dump.json'):
        os.unlink('dump.json')
        
    with SelfSyncedDict('dump.json') as index:
        for f in glob(config['source'] + '/*.md'):
            index.update(entry.convert(f))
            
    for k, v in index.iteritems():
        save(os.path.join(config['output'], k + '.html'),
             post.render(config['templates']['article'], dict(config, **v)))

    index = OrderedDict(sorted(index.items(), reverse=True))
    save(os.path.join(config['output'], 'archive.html'),
         post.render(config['templates']['archive'], 
            dict(config, **{'content': index, 'slug': 'archive'})))

    copyfile(os.path.join(config['output'], index.items()[0][0] + '.html'),
             os.path.join(config['output'], 'index.html'))

    rss(index)
    static_page()

def main(args):
    try:
        if not args:
            raise getopt.GetoptError('Error')
        opt, arg = getopt.getopt(args, 'hnrs', ['help', 'new', 'regen', 'server'])
    except getopt.GetoptError, e:
        usage()
    if arg:
        usage()
    for o, a in opt:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-n', '--new'):
            new_entry()
        elif o in ('-r', '--regen'):
            regen()
        elif o in ('-s', '--server'):
            server(config['output'], config['port'])
        else:
            usage()

config = load_config('config.json')
entry = Entry()
post = Post(config['templates']['folder'])
current_date = datetime.now().strftime('%Y-%m-%d')

if __name__ == '__main__':
    main(sys.argv[1:])