#!/usr/bin/env python
__author__ = 'heiko'
import os
import flask
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

app = flask.Flask(__name__)
articles_dir = os.path.join(app.root_path, 'wiki')
search_index = open_dir(os.path.join(app.root_path, 'index'))


@app.route('/')
def index():
    return flask.render_template('index.html', num_articles = search_index.doc_count())

@app.route('/wiki/<path:name>')
def page(name):
    if '..' in name or name.startswith('/'):
        flask.abort(404)
    try:
        return open(os.path.join(articles_dir, name)).read()
    except IOError:
        flask.abort(404)

@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.png', mimetype='image/png')


@app.route('/search')
def search():
    query_string = flask.request.args.get('search','')
    with search_index.searcher() as searcher:
        query = QueryParser("content", search_index.schema).parse(query_string)
        results = searcher.search(query)
        hits = [dict(title=r['title'], path=r['path']) for r in results]

    # do we have a perfect match?
    for hit in hits[:100]:
        if hit['title'].lower() == query_string.lower():
            return flask.redirect('wiki/' + hit['title'])
    return flask.render_template('search.html', query = query_string, results = hits)


if __name__ == '__main__':
    if len(sys.argv): # debug
        app.run(debug=True, host='0.0.0.0')
    else:
        from gevent.wsgi import WSGIServer
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
