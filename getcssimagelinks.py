#!/usr/bin/env python
'''
css files may differ between wp projects and languages
dumps all url, that need to be fetched. rewrites urls in css files.
'''

import sys, os, re
import layout

extra = ['//en.wikipedia.org/apple-touch-icon.png']

'''
fix these:
base url is dependend on site e.g.
http://bits.wikimedia.org/en.wikipedia.org/load.php?debug=false&lang=en&modules=mobile%7Cmobile.production-only%2Cproduction-jquery%7Cmobile.device.webkit&only=styles&skin=mobile&version=1352163471&*
http:../modules/images/watchlist.png
http:images/success.png
'''




def parse_css(css):
    urls = [u for u in re.findall('url\((.*?)\)', css) if not u.startswith('data:')] + extra
    for u in urls:
        print layout.norm_ext_img_url(u)
        css = css.replace(u, layout.ext_img_url2local_url(u))
    return css

def main(css_in, css_out):
    open(css_out,'w').write(parse_css(open(css_in).read()))

if __name__=='__main__':
    # urls to fetch go to stdout
    main(css_in=sys.argv[1], css_out = sys.argv[2])


