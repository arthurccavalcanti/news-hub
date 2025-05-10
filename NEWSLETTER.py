# Fontes:

bellingercat
opensecrets
piaui
marcozero
trigoeojoio
deolhonosruralistas
newyorker
bbc
brasildefato


# P.S. Copiar e colar URLs aqui.


pip install html5lib etc.
import requests
import re
from bs4 import BeautifulSoup

data = requests.get("URL")
soup = BeautifulSoup(res.content, 'html5lib')
html.parser

keywords= ['privacy','data','analytics','data science','cybersecurity']
urls = []
for key in keywords:
    html = str(soup.find_all('a', attrs = {'href':re.compile(r'^.*\b%s\b.*$' % key)}))

#find position of each href element
href_start = [s.start() for s in re.finditer('href="',html)] 
print(href_start)

# remove all urls containing special characters we don't want
if not any(c in '#?^%*()=' for c in url):
   urls.append(url)

# convert the list into a set delete all duplicates
print(set(urls))

#find elements in html
title = soup.find('h1').contents[0]

# --------------------------------------

# Using XML files (url.com/feed)
# pip install lxml

from bs4 import BeautifulSoup
import requests

url = requests.get('url.com')
soup = BeautifulSoup(url.content, 'xml')
entries = soup.find_all('entry')

for entry in entries:
    title = entry.title.text
    summary = entry.summary.text
    link = entry.link['href']
    print(f"Title: {title}\n Summary: {summary}\n Link: {link}")

# ========================

# RSS Feed Aggregator
# https://www.youtube.com/watch?v=5mEmE7pBI1A

# dependencies:
# pip3 install flask, feedparser
# (or python -m pip install flask)

from flask import Flask, render_template, request
import feedparser

# google your news sources' RSS feed URLs

app = Flask(__name__)

#dicionario de nomes e urls
RSS_FEEDS = {
    'name':'url_do_feed'
    'bbc':'url do rss feed da bbc'
}

@app.route('/')

def index():
    articles = []
    for source, feed in RSS_FEEDS.items():
        # parsed articles from feed
        parsed_feed = feedparser.parse(feed)
        # list which displays source and entry for every article
        entries = [(source, entry) for entry in parsed_feed.entries]
        # adds entries to articles list
        articles.extend(entries)

    # sorts articles by date (selects second element from tuple (i.e. entry) and extracts published_parsed element)
    # not all rss feeds have published_parsed element (find workaround)
    articles = sorted(articles, key=lambda x: x[1].published_parsed, reverse=True)

    #splits articles into html pages. default is 1. 
    page = request.args.get('page', 1, type=int)
    per_page = 10 #number of articles displayed per page.
    total_articles = len(articles)

    # start of page (starting at 0). where each page starts, given the page number and articles per page
    start = (page-1) * per_page
    # end of page
    end = start + per_page

    # articles separated per page
    paginated_articles = articles[start:end]

    # renders html page
    return render_template(template_name:'index.html', articles=paginated_articles, page=page, total_pages = ((total_articles // per_page) + 1))

@app.rout('/search')

# search for articles based on query
def search():
    query = request.args.get('q')   #gets query parameter from url
    articles = []
    
    
    for source, feed in RSS_FEEDS.items():
        # parsed articles from feed
        parsed_feed = feedparser.parse(feed)
        # list which displays source and entry for every article
        entries = [(source, entry) for entry in parsed_feed.entries]
        # adds entries to articles list
        articles.extend(entries)

    # if query is in the title of article[1] (i.e entry in tuple (source, entry)), return the article (i.e. an item in articles list)
    # both the title and query are forced to lower case (case insensitive)
    results = [article for article in articles if query.lower() in article[1].title.lower()]

    
    return render_template(template_name: 'search_results.html', articles=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)