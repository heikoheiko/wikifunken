'''

Goals:
multiple wikis can exist on the same server
Static delivery (except for search)


Relative URLs:
site/dewp/
site/enwp/articles/
site/enwp/articles/Mainz
site/enwp/articles/AC%20DC
site/enwp/images/
site/enwp/images/00016aece4b15ed6c0931ffe29b400fd.jpeg

site/enwp/index.html
site/enwp/search.py
site/enwp/jquery.js
site/enwp/styles.css



Q: Navigation?
Q: What About Categories?

All local site links are relative

Resources as seen from article are:
../images/00016aece4b15ed6c0931ffe29b400fd.jpeg
../search.py
../jquery.js
../styles.css


'''

import hashlib, os

site = 'http://en.m.wikipedia.org'

def external_wiki_link(url):
    return site + url

def external_wiki_page_link(page_name):
    return site + '/wiki/' + page_name


def norm_ext_img_url(img_src):
    if not img_src.startswith('http://'):
        img_src = 'http:%s' % img_src
    return img_src

def ext_img_url2fn(url):
    ext = url.split('.')[-1]
    return hashlib.md5(url).hexdigest() + '.' + ext

def safe_fn(fn):
    return fn.replace('/', '%2F')


def ext_img_url2local_url(img_src):
    fn = ext_img_url2fn(norm_ext_img_url(img_src))
    return '../static/images/' + fn

def stylesheet_url(num=0):
    'set debug=true for non minified view'
    ' fixed line 1137 in stylesheet0.css'
    'fixme: bg images in css need to be local'
    return '../static/stylesheet%d.css' % num

def script_url(num=0):
    'set debug=true for non minified view'
    return '../static/script%d.js' % num
