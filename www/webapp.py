#!/usr/bin/env python
__author__ = 'heiko'
import os
import flask
app = flask.Flask(__name__)
pwd = os.path.dirname(__file__)
articles_dir = os.path.join(pwd, 'articles')


@app.route('/')
def index():
    return 'Hello Homepage'


@app.route('/search/')
def search():
    query = flask.request.form['query']
    return 'Searched for %s' % query

@app.route('/wiki/<path:name>')
def page(name):
    try:
        assert not '..' in name
        return open(os.path.join(articles_dir, name)).read()
    except IOError:
        flask.abort(404)


if __name__ == '__main__':
    app.run(debug=True)