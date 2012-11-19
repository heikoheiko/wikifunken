'''

Goals:
multiple wikis can exist on the same server
Static delivery (except for search)


Relative URLs:
site/dewp/
site/enwp/articles/
site/enwp/articles/Mainz
site/enwp/articles/AC%20DC
site/enwp/images/
site/enwp/images/00016aece4b15ed6c0931ffe29b400fd.jpeg

site/enwp/index.html
site/enwp/search.py
site/enwp/jquery.js
site/enwp/styles.css



Q: Navigation?
Q: What About Categories?

All local site links are relative

Resources as seen from article are:
../images/00016aece4b15ed6c0931ffe29b400fd.jpeg
../search.py
../jquery.js
../styles.css


'''

import hashlib, os


def norm_ext_img_url(imgsrc):
    if not imgsrc.startswith('http://'):
        imgsrc = 'http:%s' % imgsrc
    return imgsrc

def ext_img_url2fn(url):
    ext = url.split('.')[-1]
    return hashlib.md5(url).hexdigest() + '.' + ext

def ext_img_url2local_url(url):
    pass

