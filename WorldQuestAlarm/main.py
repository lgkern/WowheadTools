import sqlite3
import os
import urllib
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen, urlcleanup
from urllib.error import URLError
import json
from  builtins import any as b_any
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from datetime import datetime
import asyncio

def fetch(region):
    print('>Fetching {0}'.format(region))
        
    url = 'https://www.wowhead.com/world-quests/{0}'.format(region)               
    
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

        # get text
        text = soup(["script"])

        for tag in text:
            if b_any('lvWorldQuests' in word for word in tag.contents):
                for line in tag.contents:
                    moreLines = line.split('\n')            
                    wqLines = list(filter(lambda x: 'lvWorldQuests' in x, moreLines))
                    for wqLine in wqLines:
                        _lines = wqLine.split(', data: [')
                        quests = json.loads('['+_lines[1][:-4]+']')
                        return quests

        return 'worldQuest'

def process(region, data):

    # If they reward, parse the list of quests that award each
    armyQuests = parseQuest(data, 152957)
    argussianQuests = parseQuest(data, 152960)
    quests = armyQuests + argussianQuests

    # For each quest with each id, check if it wasn't broadcasted yet
    loop =  asyncio.get_event_loop()  
    for quest in quests:
        if not checkBroadcasts( region, quest['id'], quest['ending'] ):

            # If wasn't sent, send Webhook             
            loop.run_until_complete(sendWebhook( region, quest['rewardId'], quest['id'], quest['ending'] ))  
            
            # Register the quest so it isn't sent again
            registerBroadCast( region, quest['id'], quest['ending'] )    

def parseQuest(data, rewardId):
    quests = []

    for quest in data:
        if quest['rewards']:
            for reward in quest['rewards']['items']:
                if rewardId == reward['id']:
                    quest['rewardId'] = rewardId
                    quests.append(quest)
    
    return quests

def checkBroadcasts(region, questId, endTimestamp):
    db = getDatabase()

    cursor = db.cursor()
    cursor.execute( '''SELECT 1 FROM broadcast where questId = ? and region = ? and endTimestamp = ?''', (questId, region, endTimestamp) )
    results = cursor.fetchall()

    db.commit()
    db.close()

    if results:
        return True
    else:
        return False

def registerBroadCast(region, questId, endTimestamp):
    db = getDatabase()

    cursor = db.cursor()
    cursor.execute('''INSERT INTO broadcast(questId, region, endTimestamp) VALUES(?,?,?)''', (questId, region, endTimestamp) )
    db.commit()

async def sendWebhook(region, rewardId, questId, endTimestamp):
    print('New quest found ({0}), sending Webhook'.format(questId))

    # Fetch Webhook URL
    webhookurl = ''
    with open('webhook.py') as file:
        webhookurl = file.read()        

    # Calculate time until the quest goes away
    start = datetime.now()
    end = datetime.fromtimestamp(endTimestamp / 1e3)
    duration = end - start

    faction = 'Army of the Light' if rewardId == 152957 else 'Argussian Reach'
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url('{0}'.format(webhookurl), adapter=AsyncWebhookAdapter(session))
        await webhook.send('<@118461244784115713>\n{0} - {1} Reputation - Ends in {3} Hours and {4} minutes\nQuest: http://www.wowhead.com/quest={2}'.format(region, faction, questId, duration.seconds//3600, (duration.seconds//60)%60), username='World Quest Watcher', avatar_url='https://i.imgur.com/XKQ9yMd.png')

def getDatabase():

    dbName = 'broadcasts.db'
    freshDb = os.path.isfile(dbName)
    db = sqlite3.connect(dbName)

    if not freshDb:
        cursor = db.cursor()
        cursor.execute(''' CREATE TABLE broadcast(broadcastId INTEGER PRIMARY KEY, questId INTEGER, region TEXT, endTimestamp INTEGER)''')
        db.commit()

    return db
    
loop =  asyncio.get_event_loop()  

# Fetch and Process US 
process('na', fetch('na'))

# Fetch and Process EU
process('eu', fetch('eu'))

loop.close()  