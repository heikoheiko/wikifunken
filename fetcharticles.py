#!/usr/bin/env python
import sys, os
import layout
import fetcher
import urllib2

def report_cb(status, url, fn, num, total):
    print status, fn, num, total

def main(articles_fn, out_dir):
    bot = fetcher.Fetcher(report_cb=report_cb)
    articles = open(articles_fn).readlines()
    for i,name in enumerate(articles):
        name = name.strip().decode('utf8')
        fn = os.path.join(out_dir, layout.safe_fn(name))
        if os.path.exists(fn):
            continue
        url = 'http://en.m.wikipedia.org/wiki/' + urllib2.quote(name.encode('utf8'), safe='')
        bot.add(url, fn)
    bot.run()

if __name__=='__main__':
    main(articles_fn=sys.argv[1], out_dir=sys.argv[2])

