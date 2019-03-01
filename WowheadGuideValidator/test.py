import urllib
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen, urlcleanup
from urllib.error import URLError
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

#chrome driver from https://sites.google.com/a/chromium.org/chromedriver/home
chrome_driver = os.getcwd() +"\\chromedriver.exe"

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
driver.get('https://www.wowhead.com/havoc-demon-hunter-guide')
title = driver.title.replace(' - Guides - Wowhead','')
body = driver.find_element_by_id(id_='guide-body')

driver.close()
print(title)
print(body.text)
driver.quit()

#req = Request('https://www.wowhead.com/havoc-demon-hunter-guide')
#try:
#    urlcleanup() 
#    response = urlopen(req)
#except URLError as e:
#    if hasattr(e, 'reason'):
#        print('   We failed to reach a server.')
#        print('   Reason: ', e.reason)
#    elif hasattr(e, 'code'):
#        print('    The server couldn\'t fulfill the request.')
#        print('    Error code: ', e.code)
#    
#else:
#    html = response.read()
#    soup = BeautifulSoup(html, 'html.parser')
#
#    text = ''
#    # kill all script and style elements
#    line = str(soup)
#    filters = re.findall(r'(.*)WH\.markup\.printHtml(.*?)guide-body', line)#.group(1)
#
#    content = ''
#    largest = 0
#
#    for fil in filters[0]:
#        if len(fil) > largest:
#            largest = len(fil)
#            content = fil
#
#    content = '\n'.join(content.split('\\n'))
#    content.replace('\\\r','')
#    #content = re.sub('\[(.*?)\]','',content)
#    print(html)
#    #print(fil)
#
#    # break into lines and remove leading and trailing space on each
#    lines = (line.strip() for line in text.splitlines())
#    # break multi-headlines into a line each
#    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
#    # drop blank lines
#    text = '\n'.join(chunk for chunk in chunks if chunk)
#    
#    lines = text.split('\n')
#
#    
#    # Finds the title in the text
#    title = lines[0].replace(' - Guides - Wowhead','')
#    
#    # Finds the Context - It is the line after "ReportLinks"
#    content = ''
#    nextIsContent = False
#                            
#    for line in lines:
#        if nextIsContent:
#            content += line
#        if 'ReportLinks' in line:
#            nextIsContent = True
#        if 'Share your comments about ' in line:
#            break