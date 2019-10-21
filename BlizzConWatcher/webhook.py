import sqlite3
import urllib
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen, urlcleanup
from urllib.error import URLError
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from datetime import datetime
import asyncio
import re
from databaseControls import DbApi
from botkey import Key

db = DbApi()

def fetch():
    url = 'https://blizzcon.com/en-us/news'
    
    req = Request(url)
    try:
        urlcleanup() 
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('   We failed to reach a server.')
            print('   Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('    The server couldn\'t fulfill the request.')
            print('    Error code: ', e.code)
        return None, None
    else:

        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        # get articles
        articles = soup.find_all('div', attrs={'class':'LatestNews-item'}) 

        article_titles = []
        
        for article in articles:
            title = article.find('h3', attrs={'class':'LatestNews-item-title'})
            print(title)
            article_id = re.findall(r'\b\d+\b', article.find('a').get('href'))[0]
            article_titles.append((title.string, article_id))
        
        #result_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        print(article_titles)

        return article_titles

def process(articles):

    loop =  asyncio.get_event_loop()  

    print('Processing')

    # For each article in the main page, check if it exists
    for article in articles:
        print('Checking article ', article[1])
        if db.checkChanges(article):
            print('No new article!')
            continue
        
        print('New article found')
        # If there are changes, record it and send webhook
        loop.run_until_complete( sendWebhook( article ) )  

        # Register New Article
        db.registerArticle(article)


async def sendWebhook(article):
    print('New article found, sending Webhook')

    # Fetch Webhook URL
    webhookurl = Key().webhook() 

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url('{0}'.format(webhookurl), adapter=AsyncWebhookAdapter(session))
        await webhook.send('<@118461244784115713> New BlizzCon Article published!\n<https://blizzcon.com/en-us/news/{0}>\n```{1}```'.format(article[1],article[0]), username='BlizzCon Watcher', avatar_url='https://www.telegraph.co.uk/content/dam/gaming/2017/10/13/BlizzCon-Logo_trans_NvBQzQNjv4BqutubNGxeqbD0m2XylzINLiOoem_3qpp9C-iKHR23jxY.jpg')

print('start')
loop =  asyncio.get_event_loop()  

# Fetch and Process Topics if there are filter terms
articles = fetch()
process(articles)



loop.close()  