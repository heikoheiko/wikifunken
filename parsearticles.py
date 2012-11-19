#!/usr/bin/env python
'''
http://www.w3schools.com/xpath/xpath_axes.asp
parse articles,
rewrite urls
rewrite image links
remove links
rewrite links
add link classes
'''

import sys, os
from lxml import etree
import layout


def rewrite_external_urls(troot, article_names):
    # rewrite all non local links to full url
    '''
    Within Wiki (class:localwiki):
    /wiki/Germany

    External Link (class:external):
    http://www.citymayors.com/features/quality_survey.html

    External Wiki (class:extiw):
    //wikimediafoundation.org/wiki/Terms_of_use?useformat=mobile
    http://en.m.wikipedia.org/w/index.php?title=Munich&action=history
    /w/index.php?title=Special:MobileFeedback&returnto=Munich&feedbacksource=MobileFrontend


    Interwiki Link (class:remotewiki):
    /wiki/BuxtehudeNotLocal
    /wiki/Wikipedia:General_disclaimer

    To remove links:
    http://en.wikipedia.org/w/index.php?title=Munich&mobileaction=toggle_view_desktop


    Rules:
    mw-redirect
    image
    internal
    button

    '''


    def addClass(e, cname):
        klasses = e.get('class','').split(' ')
        if not cname in klasses:
            klasses.append(cname)
            e.set('class',' '.join(x.strip() for x in klasses if x.strip()))


    for a in troot.xpath('.//a'):
  #      print
  #      print a.get('class'), a.get('href')

        url = a.get('href')
        if url.startswith('#'):
            # relative link
            pass

        elif url.startswith('//'):
            # Wikimedia Project
            a.set('href', 'http:' + url)
            addClass(a, 'extiw')
            addClass(a, 'external')

        elif url.startswith('/wiki/'):
            # Wikilink
            name = url[6:] # fixme decode
            if name in article_names:
                a.set('href', name)
                addClass(a, 'localwiki')
            else:
                a.set('href', layout.external_wiki_page_link(name))
                addClass(a, 'remotewiki')
                addClass(a, 'external')

        elif url.startswith('http'):
            # external link
            addClass(a, 'external')

        elif url.startswith('/w/'):
            # special link
            a.set('href', layout.external_wiki_link(url))
            addClass(a, 'extiw')
            addClass(a, 'external')
        elif url.startswith('ftp://'):
            pass
        else:
            #        print a, a.get('name'),  a.get('href'), [(e, e.get('class')) for e in a.xpath('ancestor-or-self::*[@class]')]
            print 'unknown', url, a.get('class')

 #       print a.get('class'), a.get('href')


def replace_image_src(troot):
    # KISS
    for i in troot.xpath('.//img'):
        # collect all images
        #print i, i.items(), [(e, e.get('class')) for e in i.xpath('ancestor-or-self::*[@class]')][-1]
        #print i.get('src')
        src = i.get('src')
#        print
#        print src
        src = layout.ext_img_url2local_url(src)
#        print src
        i.set('src', src)


def rewrite_styles(troot):
    for num,l in enumerate(troot.xpath('.//link[@rel="stylesheet"]')):
        #print i, l.get('rel'), l.get('href')
        l.set('href', layout.stylesheet_url(num))


def rewrite_scripts(troot):
    # for some reason there are no scripts in our downloads
    urls = []
    for num,l in enumerate(troot.xpath('.//script')):
        #print i, l.get('rel'), l.get('href')
        url = l.get('href')
        if url:
            urls.append(url)
            l.set('href', layout.script_url(num))
    if urls:
        print urls


def remove_language_section(troot):
    #<div class="section" id="mw-mf-language-section">
    for s in troot.xpath('.//div[@id="mw-mf-language-section"]'):
        s.xpath('..')[0].remove(s)


def remove_class_noprint(troot):
    # <div class="noprint plainlinks hlist navbar mini" style="">
    for e in troot.xpath('.//*[contains(@class, "noprint")]'):
        e.xpath('..')[0].remove(e)

def remove_ambox(troot):
    for e in troot.xpath('.//*[contains(@class, "ambox")]'):
        e.xpath('..')[0].remove(e)

def replace_menu_button(troot):
    # <a id="mw-mf-main-menu-button" class="remotewiki external" href="http://en.m.wikipedia.org/wiki/Special:MobileMenu#mw-mf-page-left" title="Open main menu">
    s = troot.xpath('.//a[@id="mw-mf-main-menu-button"]')[0]
    s.set('href', '../')
    s.set('title', 'Home')
    s.set('class', 'homelink')



def edit_search_box(troot):
    '''<form id="mw-mf-searchForm" class="search_bar" method="get" action="/w/index.php">
    '''
    s = troot.xpath('.//form[@id="mw-mf-searchForm"]')[0]
    s.set('action', '../search')




def parse_article(fn, article_names):
    parser = etree.HTMLParser()
    tree   = etree.parse(open(fn), parser)
    troot = tree.getroot()
    replace_image_src(troot)
    edit_search_box(troot)
    remove_language_section(troot)
    remove_class_noprint(troot)
    remove_ambox(troot)
    rewrite_external_urls(troot,article_names)
    replace_menu_button(troot)
    rewrite_styles(troot)
    rewrite_scripts(troot)
    return troot


def main(articles_dir, out_dir):
    articles = [x.strip() for x in os.listdir(articles_dir)]
    for name in articles:
#    for name in ['Munich']:
        fn = os.path.join(articles_dir, layout.safe_fn(name.strip()))
        print fn
        tree = parse_article(fn, articles)
        ofn = os.path.join(out_dir, layout.safe_fn(name.strip()))
        open(ofn,'w').write('<!DOCTYPE html>\n' + etree.tostring(tree))
        #open(ofn,'w').write(open(fn).read())
    return tree

if __name__=='__main__':
    tree = main(   articles_dir=sys.argv[1],
                     out_dir=sys.argv[2])


