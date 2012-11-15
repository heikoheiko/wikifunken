#!/usr/bin/env python
'''
create articles within a certain score to put in an offline distribution

Request 1:
List all projects (2000K)
http://toolserver.org/~enwp10/bin/pindex.fcgi?sec=[All]
filter for a href=http://toolserver.org/~enwp10/bin/list2.fcgi?projecta=(.*?)

Request 2:
List the X articles in project, sorted by rank
http://toolserver.org/~enwp10/bin/list2.fcgi?run=yes&projecta=Zoroastrianism&namespace=&pagename=&quality=&importance=&score=&limit=1000&offset=1&sorta=Score&sortb=Quality

'''
import sys, os
import urllib2
import re, time
from lxml import etree
from StringIO import StringIO

scores = []
fraction = 0.1
min_score = 750

def report(str):
    sys.stderr.write(str)
    sys.stderr.write('\n')

def parse_project(name, offset=0):
    time.sleep(0)
    purl = 'http://toolserver.org/~enwp10/bin/list2.fcgi?run=yes&projecta=%s&namespace=&pagename=&quality=&' + \
           'importance=&score=&limit=1000&offset=%d&sorta=Score&sortb=Quality' % (offset+1)
    url = purl % name
    report(url)
    broken_html = urllib2.urlopen(url).read()

    parser = etree.HTMLParser(encoding='utf8')
    tree   = etree.parse(StringIO(broken_html), parser)
    e = tree.getroot()
    score = 0
    for tr in e.findall('.//tr[@class="list-odd"]') + e.findall('.//tr[@class="list-even"]'):
        article = tr.find('.//a').text
        score = int(tr.find('.//td[@class="score"]').text)
        print '%d\t%s' % (score, article.encode('utf8'))
        scores.append(score)
    if score >= min_score and  'Next 1000' in broken_html:
        report('have next 1000')
        parse_project(name, offset+1000)

def suggestion():
    if scores:
        scores.sort(reverse=True)
        assert scores[0] >= scores[-1]
        return scores[int(len(scores)*fraction)]

def main():

    d = urllib2.urlopen('http://toolserver.org/~enwp10/bin/pindex.fcgi?sec=[All]').read()
    projects = re.findall(re.escape('http://toolserver.org/~enwp10/bin/list2.fcgi?projecta=') + '(.*?)"', d)

    seek = 'Bihar'
    for i, name in enumerate(projects):
        if seek and name != seek:
            continue
        else:
            seek = False
        report(str((i, len(projects), name, 'cut_off:', suggestion())))
        parse_project(name)



if __name__=='__main__':
    main()


