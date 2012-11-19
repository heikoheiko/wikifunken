#!/usr/bin/env python
import sys, os
import layout
import fetcher


def report_cb(status, url, fn, num, total):
    print status, fn, num, total

def main():
    urls_fn = sys.argv[1]
    images_dir = sys.argv[2]

    bot = fetcher.Fetcher(report_cb=report_cb)
    for i,url in enumerate(open(urls_fn)):
        url = url.strip()
        fn = os.path.join(images_dir, layout.ext_img_url2fn(url))
        if not os.path.exists(fn):
            bot.add(url, fn)
    #print bot.jobs
    bot.run()

if __name__ == '__main__':
    main()
