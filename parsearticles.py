#!/usr/bin/env python
'''
http://www.w3schools.com/xpath/xpath_axes.asp
parse articles,
rewrite urls
rewrite image links
remove links
rewrite links
add link classes
'''


import sys, os
import re, time
from lxml import etree
from fetcharticles import safe_fn

def parse_article(fn):
    parser = etree.HTMLParser()
    tree   = etree.parse(open(fn), parser)
    e = tree.getroot()
    # links
    #for a in e.xpath('.//a'):
    #    print a, a.get('name'),  a.get('href'), [(e, e.get('class')) for e in a.xpath('ancestor-or-self::*[@class]')]

    # images

    # KISS
    for i in e.xpath('.//img'):

        # collect all images
        #print i, i.items(), [(e, e.get('class')) for e in i.xpath('ancestor-or-self::*[@class]')][-1]
        print i.get('src')


def main(articles_list_fn, articles_dir, out_dir):
    articles = open(articles_list_fn).readlines()
    for name in articles:
        fn = os.path.join(articles_dir, safe_fn(name.strip()))
        print fn
        parse_article(fn)

if __name__=='__main__':
    main(articles_list_fn=sys.argv[1],
            articles_dir=sys.argv[2],
            out_dir=sys.argv[3])


