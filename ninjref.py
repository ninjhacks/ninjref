#!/usr/bin/env python3
"""
About:-
Author: sheryar (ninjhacks)
Created on : 07/05/2020
Last Update : 22/10/2020
Program : Ninjref
Version : 1.3.0
"""
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.util.retry import Retry
import os
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from optparse import OptionParser
import json

def wayBack(domain, results):
    client = "WayBack"
    printOP((client, "Start", domain))
    if options.subdomain == True:
        domain_ = "*."+domain
    else:
        domain_ = domain
    try:
        rKey =  True
        resumeKey = ""
        urlScanCount = 0
        while rKey:
            wurl = "http://web.archive.org/cdx/search/cdx?url={}/*&collapse=urlkey&output=json&fl=original&filter=~original:={}&showResumeKey=true&limit={}&resumeKey={}".format(domain_, wbFilters, WBlimit,resumeKey)
            print(wurl)
            rep = req.get(wurl, stream=True)
            if rep.status_code == 200:
                if rep.json() != []:
                    urlScanCount += 1
                    printOP((client, "urlScan "+str(urlScanCount), domain))
                    if rep.json()[-2] == []:
                        resumeKey = rep.json()[-1][0]
                        urls = [url[0] for url in rep.json()[1:-2]]
                    else:
                        rKey = False
                        urls = [url[0] for url in rep.json()[1:]]
                    urlScanWorker(urls, results, client, domain)
                else:
                    rKey = False
                    printOP((client, "Info", domain, "No Result Found"))
            else:
                rKey = False
                printOP((client, "Error", domain, response.status_code))
    except requests.RequestException as err:
        printOP((client, "Error", domain, str(err)))
    printOP((client, "End", domain))

def commonCrawl(domain, results):
    client = "commonCrawl"
    printOP((client, "Start", domain))
    if options.subdomain == True:
        domain_ = "*."+domain
    else:
        domain_ = domain
    try:
        rep = req.get(cCrawlIndexs+"?url={}/*&output=text&filter=~url:.*=&fl=url{}".format(domain_, ccFilters))
        if rep.status_code == 200:
            printOP((client, "urlScan", domain))
            urlScanWorker(rep.text.splitlines(), results, client, domain)
        elif rep.status_code != 404:
            printOP((client, "Error", domain, response.status_code))
    except requests.RequestException as err:
        printOP((client ,"Error", domain, str(err)))
    printOP((client, "End", domain))

def paramChecker(url, value):
    rep = req.get(url,allow_redirects=False)
    if value in rep.text:
        return True
    else:
        return False

def paramChanger(url, param, payload):
    urlp = urlparse(url)
    params = parse_qs(urlp.query)
    params[param] = payload
    return urlunparse((urlp.scheme, urlp.netloc, urlp.path, urlp.params, urlencode(params, doseq=True), urlp.fragment))

def urlScan(url, results, client, outputFN):
    reflParams = []
    urlp = urlparse(url)
    params = parse_qs(urlp.query)
    result = (urlp.path,*params,)
    if result not in results:
        results.add(result)
        if params:
            try:
                rep = req.get(url, allow_redirects=False)
                if len(rep.text) > 0:
                    #if any(params[param][0] in rep.text for param in params):
                    for param in params:
                        value = params[param][0]
                        if value in rep.text:
                            murl = paramChanger(url, param, payload)
                            if paramChecker(murl, payload):
                                reflParams.append(param)
                                #return True
                    if reflParams:
                        data = {'url':url,'reflparams':reflParams}
                        opWriteFile(outputDir+"/"+outputFN+'.json', json.dumps(data)+",")
                        printOP((client, "Result", str(data)))
            except requests.RequestException as err:
                printOP((client+" urlScan", "Error", url, str(err)))
    #return

def cCrawlIndex():
    client = "commonCrawl Index"
    try:
        printOP((client, "Start"))
        rep = req.get("http://index.commoncrawl.org/collinfo.json")
        if rep.status_code == 200:
            printOP((client, "End"))
            return rep.json()[0]["cdx-api"]
        else:
            printOP((client, "Error", rep.status_code))
            return False
    except requests.RequestException as err:
        printOP((client, "Error", str(err)))
        return False

def urlScanWorker(urls, results, client, domain):
    if options.output == None:
            outputFN = domain
    else:
        outputFN = options.output
    with ThreadPoolExecutor(max_workers=options.scanThreads) as threadPool:
        futures = [ threadPool.submit(urlScan, url, results, client, outputFN) for url in urls]
        wait(futures)
    #for url in urls:
    #    urlScan(url, results, client, outputFN)

def worker(domain):
    if options.output == None:
        outputFN = domain
        optSessions.append(domain)
    else:
        outputFN = options.output
    opFileHandler("create", outputFN)
    results = set()
    time.sleep(2)
    if cCrawl:
        if cCrawlIndexs:
            commonCrawl(domain, results)
        else:
            printOP(("commonCrawl", "Error", "ccIndex False"))
    if wBack:
        wayBack(domain, results)
    opFileHandler("close", domain)
    if options.output == None:
        optSessions.remove(outputFN)

def opWriteFile(file, data):
    file = open(file, 'a')
    file.write(data)
    file.close()

def opFileHandler(action, domain):
    if action == "create":
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        opWriteFile(options.outputDir+"/"+domain+'.json', "[")
    elif action == "close":
        opWriteFile(options.outputDir+"/"+domain+'.json', "{}]")             

def printOP(ops):
    if options.outputStyle == 0:
        output = "| "
        for op in ops:
            output += op+" | "
        print("| "+str(datetime.now().strftime('%H:%M:%S'))+" "+output)
    elif options.outputStyle == 1:
        if ops[1] == "Result":
            print(ops[2])
    elif options.outputStyle == 2:
        if ops[1] != "Result":
            output = "| "
            for op in ops:
                output += op+" | "
            print("| "+str(datetime.now().strftime('%H:%M:%S'))+" "+output)
    elif options.outputStyle == 3:
        if ops[1] != "Error":
            output = "| "
            for op in ops:
                output += op+" | "
            print("| "+str(datetime.now().strftime('%H:%M:%S'))+" "+output)

def header():
    os.system('clear')
    title = '''
________________________________________________________________________________
                              _  _ _ _  _  _ ____ ____ ____ 
                              |\ | | |\ |  | |__/ |___ |___ 
                              | \| | | \| _| |  \ |___ |    
________________________________________________________________________________

About:-
Author: sheryar (ninjhacks)
Version : 1.3.0
________________________________________________________________________________
    '''
    print ('\033[01;32m' + title + '\033[01;37m')

if __name__ == "__main__":
    parser = OptionParser(usage="%prog: [options]")
    parser.add_option( "-d","--domain", dest="domain", help="domain (Example : example.com)")
    parser.add_option("-f", "--file", dest="file",  help="Domains File (Example : domains.txt)")
    parser.add_option("--od", dest="outputDir", default="output", help="Output Dir (default : output)")
    parser.add_option("-o", "--output", dest="output", help="Output File (optional)")
    parser.add_option( "--sd", dest="subdomain", action='store_true', help="Subdomain (optional)")
    parser.add_option( "-p" , "--providers", dest="providers", default="wayback commoncrawl", help="Select Providers (default : wayback commoncrawl)")
    parser.add_option( "-t" , "--threads", dest="threads", default=1, type=int, help="Set main threads counts (default : 1)")
    parser.add_option( "--st", dest="scanThreads", default=10, type=int, help="Set scan threads counts (default : 10)")
    parser.add_option( "--wbf", dest="wbfilter", default="statuscode:200 ~mimetype:html", help="Set filters on wayback api (default : statuscode:200 ~mimetype:html)")
    parser.add_option( "--ccf", dest="ccfilter", default="=status:200 ~mime:.*html", help="Set filters on commoncrawl api (default : =status:200 ~mime:.*html)")
    parser.add_option( "--payload", dest="payload", default="ninjhacks", help="Payload use in scan (default : ninjhacks)")
    parser.add_option( "--wbl", dest="wbLimit", default=10000, type=int, help="Wayback results per request (default : 10000)")
    parser.add_option( "--ops", dest="outputStyle", default=0, type=int, help="Output Style (default : 0)")
    (options, args) = parser.parse_args()

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist="GET"
)
adapter = HTTPAdapter(max_retries=retry_strategy)
req = requests.Session()
req.verify = False
#req.max_redirects = 60
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
req.mount("https://", adapter)
req.mount("http://", adapter)
req.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
})

if options.outputStyle != 1:
    header()

outputDir = options.outputDir
if options.domain != None:
    domains = {options.domain}
elif options.file != None:
    dfile = open(options.file, 'r')
    domains = dfile.read().splitlines()
else:
    printOP(("System", "Error", "Domain Not Defined"))
    printOP(("System", "Info", "use -d example.com Or -f domains.txt"))
    exit()

tD = len(domains)
payload = options.payload
wbFilters = ""
ccFilters = ""
WBlimit = options.wbLimit
threadCount = options.threads
optSessions = []
cCrawl = False
wBack =  False
for provider in options.providers.split():
    if provider == "commoncrawl":
        cCrawl = True
        if options.ccfilter != None:    
            for f in options.ccfilter.split():
                ccFilters = ccFilters+"&filter="+f
    elif provider == "wayback":
        wBack = True
        if options.wbfilter != None:    
            for f in options.wbfilter.split():
                wbFilters = wbFilters+"&filter="+f
    else:
        printOP(("System", "Error", "Provider Not Found"))
        printOP(("System", "Info", "use -p wayback Or not use -p"))

if not cCrawl | wBack:
    exit()

if cCrawl:
    cCrawlIndexs = cCrawlIndex()

threadpool = ThreadPoolExecutor(max_workers=threadCount, thread_name_prefix='')
futures = [ threadpool.submit(worker, domain) for domain in domains]
try:
    for i, _ in enumerate(as_completed(futures)):
        i +=1
        printOP(("Domains","Remaning: "+str(tD-i),"Completed: "+str(i)))
except KeyboardInterrupt:
    if options.output == None:
        for domain in optSessions:
            opFileHandler("close", domain)
    else:
        opFileHandler("close", options.output)