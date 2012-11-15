#!/usr/bin/env python
"""
based on: https://github.com/gwik/geventhttpclient
"""
import sys, os, hashlib
import gevent.pool
from geventhttpclient import HTTPClient
from geventhttpclient.url import URL
user_agent = 'Wikipedia 1.0 Bot'

http_clients = dict()

def get_client(url):
    server = '/'.join(url.split('/')[:3]) + '/'
    if not server in http_clients:
        # setting the concurrency to 10 allow to create 10 connections and
        # reuse them.
        http_clients[server]  = HTTPClient.from_url(server, concurrency=10)
    return http_clients[server]

def fetch(http, url, fn, pool, num):
    # the greenlet will block until a connection is available
    #request.add_header('User-Agent',user_agent)
    response = http.get(url)
    if response.status_code == 200:
        open(fn,'w').write(response.read())
        print 'wrote', num
#        print 'pool', pool.size, len(pool), pool.free_count()
    else:
        print 'err', response.status_code, url

def url2fn(url):
    ext = url.split('.')[-1]
    return hashlib.md5(url).hexdigest() + '.' + ext

def main():
    urls_fn = sys.argv[1]
    images_dir = sys.argv[2]

    # allow to run 20 greenlet at a time, this is more than concurrency
    # of the http client but isn't a problem since the client has its own
    # connection pool.
    pool = gevent.pool.Pool(20)

    for i,url in enumerate(open(urls_fn)):  
	#if i> 400: break
        url = url.strip()
        fn = os.path.join(images_dir, url2fn(url))
        if not os.path.exists(fn):
            http = get_client(url)
            pool.spawn(fetch, http, url, fn, pool, i)

    pool.join()
    for http in http_clients.values():
        http.close()

if __name__ == '__main__':
    main()
