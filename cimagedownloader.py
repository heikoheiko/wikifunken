#!/usr/bin/env python
"""
based on: https://github.com/gwik/geventhttpclient
"""
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

def fetch(http, url, fn):
    # the greenlet will block until a connection is available
    #request.add_header('User-Agent',user_agent)
    response = http.get(url)
    assert response.status_code == 200
    print dir(response), fn

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

    for url in open(urls_fn)[:200]:
        url = url.strip()
        fn = os.path.join(images_dir, url2fn(url))
        if not os.path.exists(fn):
            http = get_client(url)
            print url, http
            pool.spawn(fetch, http, url, fn)

    pool.join()
    for http in http_clients:
        http.close()

if __name__ == '__main__':
    main()