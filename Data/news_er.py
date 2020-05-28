import pandas as pd
import numpy as np
from eventregistry import *

# Get key at http://eventregistry.org/register
# Look for API key in profile page
myKey = ''
er = EventRegistry(apiKey = myKey)

# create new query object
q_neg = QueryArticlesIter(
        keywords = QueryItems.AND(["reopen", "coronavirus"]), # substitute with any keyword(s)
        sourceUri = QueryItems.OR(["cnn.com", "nytimes.com", "msnbc.com"]), # substitute with any url(s)
        dateStart = "2020-05-05", # substitute with any date range(s)
        dateEnd = "2020-05-11",
        keywordsLoc = "body", # "body" or "title"
        minSentiment = -1, # int in [-1,1]
        maxSentiment = 0,
        dataType = "news")

neg_count = 0

# get each article and print
for article in q_neg.execQuery(er, sortBy = "rel", 
        returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(authors = False, eventUri = False, body = False, sentiment = True)),
        maxItems = 999999):
    print(article)
    neg_count = neg_count + 1

print(f"Negative sentiment: {neg_count} articles found.")

q_pos = QueryArticlesIter(
        keywords = QueryItems.AND(["reopen", "coronavirus"]),
        sourceUri = QueryItems.OR(["cnn.com", "nytimes.com", "msnbc.com"]),
        dateStart = "2020-05-05",
        dateEnd = "2020-05-11",
        keywordsLoc = "body",
        minSentiment = 0,
        maxSentiment = 1,
        dataType = "news")

pos_count = 0

for article in q_pos.execQuery(er, sortBy = "rel", 
        returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(authors = False, eventUri = False, body = False, sentiment = True)),
        maxItems = 999999):
    print(article)
    pos_count = pos_count + 1

print(f"Positive sentiment: {pos_count} articles found.")