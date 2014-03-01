wikifunken - OpenWRT Wikipedia Offline Server
=============================================

This projects provides software to serve Wikipedia from a cheap OpenWRT powered router (like the TP-Link TL-WR703N).

Could be used to set up a $25 hotspot and serve Wikipedia in rural areas. 


It provides tools to:
 * score and select a subset of wikipedia articles 
 * fetch the articles
 * parse & rewrite artciles 
 * fetch the images
 * index the articles
 * pack the data in a SquashFS (read only compressed) filesystem
 * info on the OpenWRT configuration

Note: I hacked this since the Kiwix http server used to much resources to run on small hardware. The system basically worked and was tested with 50K articles. The whole thing is undocumented. Contact me if you are interested in using it and need help to get started. 


Documentation
-------------

# Wikipeda Version 1.0 Project  http://en.wikipedia.org/wiki/Wikipedia:Version_1.0_Editorial_Team
# is not on toolserver anumore FIXME

# Select NUM=1000 articles to download and select
~/dev/wikifunken/ ./articleselector.py scored_articles.15.11.12.txt 1000 > data/articles.txt
selected 1000 of 1139809 articles with minimum rank 1846

# Fetch articles
~/dev/wikifunken/ ./fetcharticles.py data/articles.txt data/articles/

# fetch images
~/dev/wikifunken/ ./getimagelinks.py data/articles/ | sort | uniq > data/images.txt



# define layout

# Process Articles
# rewrites links, removes unwanted sections, ...

# index articles


Unlicense
-------
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>