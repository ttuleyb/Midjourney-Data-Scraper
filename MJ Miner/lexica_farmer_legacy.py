from imp import load_source
import os
import json
from urllib import request
from xmlrpc.client import loads
from requests import get
from multiprocessing.pool import ThreadPool
import random
import time

##TODO MAKE ANOTHER LOOP THAT SPECIFICALLY RE REQUESTS FILES UNDER 50KB 
##AS THEY ARE EITTHER FULL OR PARTIAL ERRORS

MAX_THREADS = 12

def squareBracketFinder(data):
    first = data.index("[")
    data = data[first:]
    last = data.rfind("]")
    data = data[:last+1]
    return data

def setRequestPrefix():
    global requestPrefix
    global pageEnd
    if prefix == "n_":
        requestPrefix = "new"
        pageEnd = 5000
    elif prefix == "h_":
        requestPrefix = "hot"
        pageEnd = 3000
    elif prefix == "r_":
        requestPrefix = "rising"
        pageEnd = 2500
    elif prefix == "tt_":
        requestPrefix = "top-today"
        pageEnd = 5000
    elif prefix == "tm_":
        requestPrefix = "top-month"
        pageEnd = 2500
    elif prefix == "tw_":
        requestPrefix = "top-week"
        pageEnd = 500

waitForServer = False

everything = []
pageArray = []
prefix = "h_"

pageEnd = 2750
requestPrefix = "top-all"
setRequestPrefix()

#More info:
#When sorting by new, every 1000 page seems to equal 5 hours
#Here are the page number limits by different sorting methods
#New: 5000+ Top-all: 2750~ Hot: 3000+ Rising: 2500+ Top-today: 5000+ I am still not completely sure, should do more tests after scraping is done

def getStuff(page):
    #rising, hot, new, top-week, top-today, top-month, top-all
    #top-all is default
    #otherwise, r_, h_, n_, tw_, tt_, tm_, ta_
    #change prefix
    global prefix
    global requestPrefix
    global waitForServer
    if waitForServer:
        waitForServer = False
    request = f"https://www.midjourney.com/api/app/recent-jobs/?amount=250&jobType=upscale&orderBy={requestPrefix}&jobStatus=completed&page={page}&dedupe=true&refreshApi=0"
    headerss = {
        'authority': 'www.midjourney.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '^\\^',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '__Secure-next-auth.session-token=INSERT_HERE',
    }
    cookiess = {
        '__Secure-next-auth.session-token': 'INSERT_HERE'
    }
    try:
        r = get(request, headers=headerss, cookies=cookiess, timeout=45)
        #asd = (str(r.content))
        contents = str(r.content.decode('utf-8'))
        if len(contents) < 10000:
            waitForServer = True
            print("Invalid Response")
        else:
            print("Valid Response")
            with open("jsons\\" + prefix + str(page) + ".json", "w", encoding="utf-8") as f:
                f.write(contents)
    except:
        print("error")
        waitForServer = True
    # data = loads(asd)
    # global everything
    # for i in data[0]["result"]["data"]["json"]["prompts"]:
    #     everything.append([i["prompt"], i["model"]])

lastPage = 1

while lastPage < pageEnd:
    pageArray = []
    for i in range(100):
        filename = "jsons\\" + prefix + str(i+lastPage) + ".json"
        if os.path.exists(filename) and os.path.getsize(filename) > 10000:
            continue
        pageArray.append(i + lastPage)
        print(i + lastPage)
    lastPage += 100

    with ThreadPool(MAX_THREADS) as p:
        p.map(getStuff, pageArray)

print()