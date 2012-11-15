#!/usr/bin/env python
'''

>>> from whoosh.fields import *
>>> schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
>>> ix = create_in("indexdir", schema)
>>> writer = ix.writer()
>>> writer.add_document(title=u"First document", path=u"/a",
...                     content=u"This is the first document we've added!")
>>> writer.add_document(title=u"Second document", path=u"/b",
...                     content=u"The second one is even more interesting!")
>>> writer.commit()
>>> from whoosh.qparser import QueryParser
>>> with ix.searcher() as searcher:
...     query = QueryParser("content", ix.schema).parse("first")
...     results = searcher.search(query)
...     results[0]
...
{"title": u"First document", "path": u"/a"}
'''
import sys, os
import urllib2
import time
from lxml import etree

from whoosh.index import create_in
from whoosh.fields import TEXT, ID, Schema
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)


def safe_fn(fn):
    return fn.replace('/', '%2F')

def get_text(fn):
    parser = etree.HTMLParser()
    tree   = etree.parse(open(fn), parser)
    e = tree.getroot()
    '''
    The Language Section should already be killed!
    <div class="section" id="mw-mf-language-section">

    Main Content:
    e.xpath('.//div[@class="show "]//text()')
    '''
    text = u''.join(e.xpath('.//div[@class="show "]//text()'))
    return text



def main(articles_fn, articles_dir, index_dir):
    ix = create_in(index_dir, schema)
    writer = ix.writer()

    articles = open(articles_fn).readlines()
    for i,name in enumerate(articles):
        name = name.strip().decode('utf8')
        fn = os.path.join(articles_dir, safe_fn(name))
        if not os.path.exists(fn):
            print 'not there', fn
            continue
        else:
            print 'indexing', fn
        text = get_text(fn)
#        print text[:400]
        writer.add_document(title=name, path=fn, content=text)

    writer.commit()
    print '%d docs in index' % ix.doc_count()


if __name__=='__main__':
    main(articles_fn=sys.argv[1], articles_dir=sys.argv[2], index_dir=sys.argv[3])

