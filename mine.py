import feedparser
import json
import re
import uuid
from elasticsearch import Elasticsearch

es = Elasticsearch()
content = feedparser.parse("http://feeds.bbci.co.uk/indonesia/rss.xml")  # News resource or link

# create a function to remove the html syntax from the news

def cleanhtml(raw_html):  
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

data = ''

n = {}

# formatting the data to be indexed into elasticsearch

for item in content.entries:
    _id = uuid.uuid4()
    data += '{"index": {"_id": "%s"}}\n' % _id
    data += json.dumps({
        "source": "detik.com",
        "title": item.title,
        "link": item.link,
        "description": item.description,
        "date": item.published
    }) + '\n'
    
# indexing the data into elasticsearch
    es.bulk(index='news', doc_type='rss-feeds', body=cleanhtml(data))

