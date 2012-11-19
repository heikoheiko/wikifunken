#!/usr/bin/env python
'''
simply dump all image links

Stats:

1K Articles:
61K Images
25K Uniq Images
./getimagelinks.py m.en/articles |sort|uniq> imagelinks.txt


'''

import sys, os
from lxml import etree
import layout



def parse_article(fn):
    parser = etree.HTMLParser()
    tree   = etree.parse(open(fn), parser)
    e = tree.getroot()
    for i in e.xpath('.//img'):
        try:
            print layout.norm_ext_img_url(i.get('src'))
        except UnicodeEncodeError:
            sys.stderr.write('UnicodeError %s %r \n' %(fn, i.get('src')))

def main(articles_dir):
    for name in os.listdir(articles_dir):
        fn = os.path.join(articles_dir,name.strip())
        parse_article(fn)

if __name__=='__main__':
    main(articles_dir=sys.argv[1])


