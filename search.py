#!/usr/bin/env python
'''
pip install whoosh
'''
import sys
from whoosh.index import open_dir
from whoosh.qparser import QueryParser


def suggest(ix, term):
    s = ix.searcher()
    c = s.corrector('title') # just use page titles as dictionary
    return c.suggest(term.lower(), limit=50, maxdist=20, prefix=len(term)) # will be all lowercase

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


