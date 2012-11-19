#!/usr/bin/env python
"""
based on: https://github.com/gwik/geventhttpclient
"""
import sys, os, hashlib
import gevent.pool
from geventhttpclient import HTTPClient
import layout
#user_agent = 'Wikipedia 1.0 Bot'



class Fetcher(object):
    concurrency = 10

    def __init__(self, report_cb):
        self.pool = gevent.pool.Pool(20)
        self.http_clients = dict()
        self.report_cb = report_cb
        self.counter = 0
        self.jobs = 0

    def add(self, url, out_fn):
        self.jobs += 1
        self.pool.spawn(self.fetch, url, out_fn)

    def get_client(self,url):
        server = '/'.join(url.split('/')[:3]) + '/'
        if not server in self.http_clients:
            self.http_clients[server]  = HTTPClient.from_url(server, concurrency=self.concurrency)
        return self.http_clients[server]

    def fetch(self, url, fn):
        # the greenlet will block until a connection is available
        #request.add_header('User-Agent',self.user_agent)
        http = self.get_client(url)
        response = http.get(url)
        self.counter += 1
        if response.status_code == 200:
            open(fn,'w').write(response.read())
        self.report_cb(response.status_code, url,fn, self.counter, self.jobs)

    def run(self):
        self.pool.join()
        for http in self.http_clients.values():
            http.close()

