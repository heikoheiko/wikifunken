#!/usr/bin/env python
'''
'''
import sys, os
import urllib2
import time
from lxml import etree

from whoosh.index import open_dir
from whoosh.fields import TEXT, ID, Schema
from whoosh.qparser import QueryParser
from indexarticles import schema

def main(index_dir, query_string):

    ix = open_dir(index_dir)
    print '%d docs in index' % ix.doc_count()

    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_string)
        print 'Q:', query
        results = searcher.search(query)
        print 'R:', results
        for r in results:
            print r



    return ix

if __name__=='__main__':
    ix = main(index_dir=sys.argv[1], query_string=u' '.join(x.decode('utf8') for x in sys.argv[2:]))


