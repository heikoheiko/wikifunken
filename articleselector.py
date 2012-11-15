#!/usr/bin/env python
'''
take article list and sort it

different projects give different scores to articles. what to do? give it a max?

what is the max score for some lame football player in that project:
http://toolserver.org/~enwp10/bin/list2.fcgi?run=yes&projecta=College_basketball&namespace=&pagename=&quality=&importance=&score=&limit=250&offset=1&sorta=Score&sortb=Quality

whatever

'''
import sys, os
import urllib2
import re, time
from lxml import etree
from StringIO import StringIO


def main(fn, num):
    scores = []
    for l in open(fn):
        score, name = l.strip().split('\t')
        scores.append((int(score),name))
    scores.sort(reverse=True)
    seen = set()
    uniq = []
    for score,name in scores:
        if name not in seen:
            uniq.append((score, name))
            seen.add(name)

    navailable = len(uniq)
    uniq = uniq[:min(num,navailable)]
    sys.stderr.write('selected %d of %d articles with minimum rank %d\n' %(len(uniq), navailable, uniq[-1][0]))
    for score, name in uniq:
        print name


if __name__=='__main__':
    main(fn=sys.argv[1], num=int(sys.argv[2]))


