wikifunken
==========

Tools to bring Wikipedia Offline





# Select NUM=1000 articles to donload and select
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
#


