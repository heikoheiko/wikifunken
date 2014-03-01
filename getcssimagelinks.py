#!/usr/bin/env python
'''
css files may differ between wp projects and languages
dumps all url, that need to be fetched. rewrites urls in css files.
'''

import sys, os, re
import layout
import urllib2

extra = ['//en.wikipedia.org/apple-touch-icon.png']

'''
fix these:
base url is dependend on site e.g.
http://bits.wikimedia.org/en.wikipedia.org/load.php?debug=false&lang=en&modules=mobile%7Cmobile.production-only%2Cproduction-jquery%7Cmobile.device.webkit&only=styles&skin=mobile&version=1352163471&*
http:../modules/images/watchlist.png
http:images/success.png
'''




def parse_css(css, cssimagedir):
    urls = [u for u in re.findall('url\((.*?)\)', css) if not u.startswith('data:')] + extra
    for u in urls:
        url = layout.norm_ext_img_url(u)
        lurl = layout.ext_img_url2local_cssimg_url(url)
        fn = layout.ext_img_url2fn(url, keep_ext=False)
        ofn = os.path.join(cssimagedir, fn)
        #print url, lurl, fn, ofn
        try:
            open(ofn, 'w').write( urllib2.urlopen(url).read() )
            css = css.replace(u, lurl)
        except urllib2.URLError, e:
            print 'ERR', e, url
    return css

def main(css_in, css_out, cssimagedir):
    open(css_out,'w').write(parse_css(open(css_in).read(), cssimagedir))

if __name__=='__main__':
    # urls to fetch go to stdout
    main(css_in=sys.argv[1], css_out = sys.argv[2], cssimagedir = sys.argv[3])


