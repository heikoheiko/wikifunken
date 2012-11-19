#!/usr/bin/env python
'''

'''
import sys, os
import urllib2
import time
from lxml import etree

from whoosh.index import create_in
from whoosh.fields import TEXT, ID, Schema
import layout

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
# http://andrewwilkinson.wordpress.com/2011/10/13/beating-google-with-couchdb-celery-and-whoosh-part-6/
# rank=NUMERIC(stored=True, type=float),

def get_text(fn):
    parser = etree.HTMLParser()
    tree   = etree.parse(open(fn), parser)
    e = tree.getroot()
    '''
    Main Content:
    e.xpath('.//div[@class="show "]//text()')
    '''
    text = u''.join(e.xpath('.//div[@class="show "]//text()')) # OPTIMIZE ME
    return text



def main(articles_fn, articles_dir, index_dir):
    ix = create_in(index_dir, schema)
    writer = ix.writer()

    articles = open(articles_fn).readlines()
    for i,name in enumerate(articles):
        name = name.strip().decode('utf8')
        fn = os.path.join(articles_dir, layout.safe_fn(name))
        if not os.path.exists(fn):
            print 'not there', fn
            continue
        else:
            print 'indexing', fn
        text = get_text(fn)
#        print text[:400]
        writer.add_document(title=name, path=fn, content=text)

    writer.commit(optimize=True) # optimize did not result in any size improvements
    print '%d docs in index' % ix.doc_count()


if __name__=='__main__':
    main(articles_fn=sys.argv[1], articles_dir=sys.argv[2], index_dir=sys.argv[3])

