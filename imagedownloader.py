#!/usr/bin/env python
"""This is a recursive web crawler.  Don't go pointing this at random sites;
it doesn't respect robots.txt and it is pretty brutal about how quickly it
fetches pages.

The code for this is very short; this is perhaps a good indication
that this is making the most effective use of the primitves at hand.
The fetch function does all the work of making http requests,
searching for new urls, and dispatching new fetches.  The GreenPool
acts as sort of a job coordinator (and concurrency controller of
course).

!!!! alternative: https://github.com/gwik/geventhttpclient
"""
from __future__ import with_statement

from eventlet.green import urllib2
import eventlet
import sys, os, hashlib, time

pool_size = 5
pool = eventlet.GreenPool(pool_size)
user_agent = 'Wikipedia 1.0 Bot'

class TimeoutException(Exception):
        pass

def fetch((url, fn), urlfns):
    print 'pool', pool.running(), pool.waiting()
    print len(urlfns), "fetching", url
    try:
        with eventlet.Timeout(5, TimeoutException):
            request = urllib2.Request(url)
            request.add_header('User-Agent',user_agent)
            opener = urllib2.build_opener()
            try:
                res = opener.open(request)
                open(fn, 'w').write(res.read())
            except urllib2.HTTPError, e:
                print e, url
        if urlfns:
            pool.spawn_n(fetch, urlfns.pop(), urlfns)
    except TimeoutException:
        # retry
        print 'timeout', url
        pool.spawn_n(fetch, (url, fn), urlfns)

def fetchall(urlfns):
    for i in range(pool_size):
        pool.spawn_n(fetch, urlfns.pop(), urlfns)
    pool.waitall()

def url2fn(url):
    ext = url.split('.')[-1]
    return hashlib.md5(url).hexdigest() + '.' + ext


def main():
    urls_fn = sys.argv[1]
    images_dir = sys.argv[2]
    urlfns = []
    for url in open(urls_fn):
        url = url.strip()
        fn = os.path.join(images_dir, url2fn(url))
        if not os.path.exists(fn):
            urlfns.append((url, fn))
    fetchall(urlfns)


if __name__ == '__main__':
    main()
