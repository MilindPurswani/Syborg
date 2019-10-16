from threading import Thread
import sys
from filequeue import *
import sys
import socket
import dns.resolver
import argparse
import time
import random
import string



def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def getTime():
    return time.strftime("%Y:%m:%d - %H:%M:%S")

def printVerbose(message):
    if args.verbose:
        print(message)


def doWork():
    while True:
        word = q.get()
        getStatus(word)
        q.task_done()
        if q.empty():
            #print("empty queue")
            pass

def checkwildcard(domain):
    a = randomString()
    temp_domain = a + '.'+ domain
    result = checkrandom(temp_domain)
    if(result == "resolved" or result == "noanswer"):
        return False
    else:
        return True

def warning():
    return "\033[1;31;40m[*]["+getTime()+"] "

def error():
    return "\033[0m 0;37;40m[*]["+getTime()+"] "

def info():
    return "\033[0;37;40m[*]["+getTime()+"] "

def success():
    return"\033[1;32;40m[*]["+getTime()+"] "


def checkrandom(domain):
    try:
        answers = dns.resolver.query(domain)
        return "resolved"
    except dns.resolver.Timeout:
        return "timeout"
    except dns.resolver.NXDOMAIN:
        return "nxdomain"
    except dns.resolver.NoAnswer:
        return "noanswer"
    except dns.exception.DNSException:
        return "unknown exception"

def getStatus(domain):
    try:
        answers = dns.resolver.query(domain)
        #for rdata in answers: # for each response
            #print("Resolved " + domain + " : " +str(rdata)) # print the data
        appenddataset1(domain) 
        printVerbose(success()+"Resolved domain %s" % domain)
        print(domain)
        log("Resolved domain %s" % domain)
        out_file.write(domain+"\n")
    except dns.resolver.Timeout:
        printVerbose(warning()+"Timeout for domain %s" % domain)        
        addbacktoqueue(domain)
        log("Timeout for domain %s" % domain)
    except dns.resolver.NXDOMAIN:
        printVerbose(info()+"No such domain %s" % domain)
        log("No such domain %s" % domain)
    except dns.resolver.NoAnswer:      
        printVerbose(success()+"Not resolved %s" % domain)
        appenddataset1(domain)
        log("Not resolved %s" % domain)
    except dns.exception.DNSException:
        #print("Unhandled exception")
        log("DNS Exception %s" % domain)
        printVerbose("DNS Exception %s" % domain)

def checkdomain():
    result = checkrandom(site)
    printVerbose("Checkrandom returned: "+result)
    if(result == "resolved" or result == "noanswer"):
        print("calling appenddataset1")
        appenddataset(site)
    elif(result == "timeout"):
        print("Internet Connection issues")
    else:
        pass

def appenddataset(domain):
    try:
        if checkwildcard(domain):
            for words in open(wordlist ,'r'):
                q.put(words.strip() + "." + domain)
            pass
        q.join()    
    except:
        print("unexpected error")
        log("unexpected error")


def appenddataset1(domain):
    try:
        if checkwildcard(domain):
            print("addding to queue")
            for words in open(wordlist ,'r'):
                q.put(words.strip() + "." + domain)
    except exception as e:
        print(e)
        log(e)
        
failed_dict = {}

def addbacktoqueue(domain):
    if domain in failed_dict:
        if failed_dict[domain] >= threshold:
            if args.enablelogging:
                log("Not putting %s into queue [Failed attempts exceeded]" % domain)
            printVerbose("Not putting %s into queue [Failed attempts exceeded]" % domain)
        else:
            failed_dict[domain] += 1
            q.put(domain)
    else:
        failed_dict[domain] = 1
        q.put(domain)


parser = argparse.ArgumentParser()
parser.add_argument("domain",help="domain name of the target")
parser.add_argument("-d","--dns",help="DNS Server to be used (default: 8.8.8.8)")
parser.add_argument("-w","--wordlist",help="Specify a custom wordlist (default: wordlist.txt)")
parser.add_argument("-o","--output",help="Specify the output file (default: results-domain.txt)")
parser.add_argument("-c","--concurrency",help="Specify the level of concurrency (default: 10)")
parser.add_argument("-l","--enablelogging",help="Enable logging to a file",action="store_true")
parser.add_argument("-v", "--verbose", help="increase output verbosity",action="store_true")
parser.add_argument("-t", "--threshold", help="Number of times to retry domain incase of timeout(default: 3)")
args = parser.parse_args()
site = args.domain

if args.dns:
    dns_server = args.dns
else:
    dns_server = "8.8.8.8"

if args.threshold:
    threshold = int(args.threshold)
else:
    threshold = 3

if args.output:
    output_file = args.output
else:
    output_file = "results-"+site+".txt"

out_file = open(output_file,"a")

if args.wordlist:
    wordlist = args.wordlist
else:
    wordlist = "wordlist.txt"

if args.concurrency:
    concurrent = int(args.concurrency,10)
else:
    concurrent = 10



printVerbose("[*]["+getTime()+"] Starting Scan against %s " % site)
printVerbose("[*]["+getTime()+"] Verbose Mode On!")
printVerbose("[*]["+getTime()+"] DNS Server Set to %s" % dns_server)
printVerbose("[*]["+getTime()+"] Output to %s" % output_file)
printVerbose("[*]["+getTime()+"] BEWARE: This may overwrite the file if it's already existing.")
printVerbose("[*]["+getTime()+"] Using wordlist %s" % wordlist)
printVerbose("[*]["+getTime()+"] Concurrency set to %s" % concurrent)


def log(data):
    if args.enablelogging:
        logfile.write(data+"\n")

if args.enablelogging:
    log_file = output_file+"-"+"log.log"
    logfile = open(log_file,"a+")
    printVerbose("[*]["+getTime()+"] Logging to file %s" % log_file)
    log("[*]["+getTime()+"] Logging to file %s" % log_file)



log("[*]["+getTime()+"] Starting Scan against %s " % site)
log("[*]["+getTime()+"] Verbose Mode On!")
log("[*]["+getTime()+"] DNS Server Set to %s" % dns_server)
log("[*]["+getTime()+"] Output to %s" % output_file)
log("[*]["+getTime()+"] BEWARE: This may overwrite the file if it's already existing.")
log("[*]["+getTime()+"] Using wordlist %s" % wordlist)
log("[*]["+getTime()+"] Concurrency set to %s" % concurrent)

#Delay the script from running to allow users to read options
if args.verbose:
    time.sleep(2)

resolver = dns.resolver.Resolver()
resolver.nameservers = [socket.gethostbyname(dns_server)]
resolver.timeout = 1
resolver.lifetime = 1

q = filequeue.FileQueue(maxsize=1000)
try:
    file = open(output_file,"w+")
except exception as e:
    print(e)
    log(e)    
    exit(1)

for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()

checkdomain()

out_file.close()
if args.enablelogging:
    logfile.close()