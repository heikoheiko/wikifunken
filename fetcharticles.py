#!/usr/bin/env python
'''


'''
import sys, os
import urllib2
import time


user_agent = 'WP1.0 Bot - fetching 100K articles from cache / report problems to pediapress '
user_agent = 'Python-urllib/2.6'
fetch_delay = 0.

def safe_fn(fn):
    return fn.replace('/', '%2F')

def fetch(name):
    url = 'http://en.m.wikipedia.org/wiki/' + urllib2.quote(name, safe='')
    print 'fetching', url
    req = urllib2.Request(url, headers={'User-Agent':user_agent})
    res = urllib2.urlopen(req)
    return res.read()

def main(articles_fn, out_dir):
    articles = open(articles_fn).readlines()
    for i,name in enumerate(articles):
        name = name.strip().decode('utf8')
        fn = os.path.join(out_dir, safe_fn(name))
        print i, len(articles), name, fn

        if os.path.exists(fn):
            print 'already there', fn
            continue
        try:
            html = fetch(name)
        except (urllib2.HTTPError,KeyError, urllib2.URLError) , e:
            print e
            continue
        open(fn, 'w').write(html)
        time.sleep(fetch_delay)


if __name__=='__main__':
    main(articles_fn=sys.argv[1], out_dir=sys.argv[2])

