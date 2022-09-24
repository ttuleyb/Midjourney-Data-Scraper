from email import header
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

def setRequestPrefix(prefixx):
    global requestPrefix
    global pageEnd
    global prefix

    if prefixx == "n_":
        prefix = "n_"
        requestPrefix = "new"
        pageEnd = 5000
    elif prefixx == "h_":
        prefix = "h_"
        requestPrefix = "hot"
        pageEnd = 4000
    elif prefixx == "r_":
        prefix = "r_"
        requestPrefix = "rising"
        pageEnd = 3500
    elif prefixx == "tt_":
        prefix = "tt_"
        requestPrefix = "top-today"
        pageEnd = 6000
    elif prefixx == "tm_":
        prefix = "tm_"
        requestPrefix = "top-month"
        pageEnd = 3500
    elif prefixx == "tw_":
        prefix = "tw_"
        requestPrefix = "top-week"
        pageEnd = 1500
    elif prefixx == "ta_":
        prefix = "ta_"
        requestPrefix = "top-all"
        pageEnd = 3750

request_dict = {'ta_':["top-all", 2750], 'tw_':["top-week", 2000], 'tm_':["top-month", 2572], 'tt_':["top-today", 5000], 'h_':["hot", 3000], 'n_':["new", 5000], 'r_':["rising", 2600]}

everything = []
pageArray = []
prefix = "Error"

#pageEnd = 2750
requestPrefix = "top-all"

#More info:
#When sorting by new, every 1000 page seems to equal 5 hours
#Here are the page number limits by different sorting methods
#New: 5000+ Top-all: 2750~ Hot: 3000+ Rising: 2500+ Top-today: 5000+ I am still not completely sure, should do more tests after scraping is done

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

waitForServer = False
MAX_THREADS = 1

def getStuff(info):
    time.sleep(2)
    #rising, hot, new, top-week, top-today, top-month, top-all
    #top-all is default
    #otherwise, r_, h_, n_, tw_, tt_, tm_, ta_
    #change prefix
    global requestPrefix
    global waitForServer
    page = info[0]
    prefix = info[1]
    requestPrefix = request_dict[prefix][0]
    request = f"https://silenus.midjourney.com/api/app/recent-jobs/?amount=250&jobType=upscale&orderBy={requestPrefix}&jobStatus=completed&page={page}&dedupe=true&refreshApi=0"
    
    global cookiess
    global headerss

    if waitForServer:
        time.sleep(60)
        waitForServer = False

    try:
        r = get(request, headers=headerss, cookies=cookiess, timeout=45)
        #asd = (str(r.content))
        contents = str(r.content.decode('utf-8'))
        if "Internal server error" in contents:
            print("Internal Error")
            waitForServer = True

        if len(contents) < 10000:
            waitForServer = True
            #print("Invalid Response")
        else:
            #print("Valid Response")
            with open("jsons\\" + prefix + str(page) + ".json", "w", encoding="utf-8") as f:
                f.write(contents)
    except:
        print("error")
        waitForServer = True
    # data = loads(asd)
    # global everything
    # for i in data[0]["result"]["data"]["json"]["prompts"]:
    #     everything.append([i["prompt"], i["model"]])

def runScraper():
    lastPage = 1
    batch_size = 50

    while lastPage < 50:
        pageArray = []
        for prefix in request_dict:
            for i in range(batch_size):
                if i+lastPage > 50: #request_dict[prefix][1]:
                    break

                filename = "jsons\\" + prefix + str(i+lastPage) + ".json"
                if os.path.exists(filename) and os.path.getsize(filename) > 10000:
                    continue
                pageArray.append([i + lastPage, prefix])
            print(f"{prefix} {lastPage} - {lastPage + batch_size}")
            with ThreadPool(MAX_THREADS) as p:
                p.map(getStuff, pageArray)
        lastPage += batch_size

import time
import datetime

def time_until_end_of_day(dt=None):
    # type: (datetime.datetime) -> datetime.timedelta
    """
    Get timedelta until end of day on the datetime passed, or current time.
    """
    if dt is None:
        dt = datetime.datetime.now()
    tomorrow = dt + datetime.timedelta(days=1)
    return datetime.datetime.combine(tomorrow, datetime.time.min) - dt


while True:
    for i in range(1):
        if time_until_end_of_day().total_seconds() < 3600:
            break
        runScraper()

    print("Archiving...")
    import archiver

    print("Done!")
    print("Waiting " + str(time_until_end_of_day().total_seconds()) + " seconds")

    time.sleep(time_until_end_of_day().total_seconds())
