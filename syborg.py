from threading import Thread
import sys
from filequeue import *
import sys
import socket
import dns.resolver
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("domain",help="domain name of the target")
parser.add_argument("-d","--dns",help="DNS Server to be used (default: 8.8.8.8)")
parser.add_argument("-w","--wordlist",help="Specify a custom wordlist (default: wordlist.txt)")
parser.add_argument("-o","--output",help="Specify the output file (default: results-domain.txt)")
parser.add_argument("-c","--concurrency",help="Specify the level of concurrency (default: 10)")
parser.add_argument("-l","--enablelogging",help="Enable logging to a file",action="store_true")
parser.add_argument("-v", "--verbose", help="increase output verbosity",action="store_true")
args = parser.parse_args()
site = args.domain

if args.dns:
    dns_server = args.dns
else:
    dns_server = "8.8.8.8"

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
    concurrent = args.concurrency
else:
    concurrent = 10

    
def getTime():
    return time.strftime("%Y:%m:%d - %H:%M:%S")


if args.verbose:
    print("[*]["+getTime()+"] Starting Scan against %s " % site)
    print("[*]["+getTime()+"] Verbose Mode On!")
    print("[*]["+getTime()+"] DNS Server Set to %s" % dns_server)
    print("[*]["+getTime()+"] Output to %s" % output_file)
    print("[*]["+getTime()+"] BEWARE: This may overwrite the file if it's already existing.")
    print("[*]["+getTime()+"] Using wordlist %s" % wordlist)
    print("[*]["+getTime()+"] Concurrency set to %s" % concurrent)

def log(data):
    if args.enablelogging:
        logfile.write(data+"\n")

if args.enablelogging:
    log_file = output_file+"-"+"log.log"
    logfile = open(log_file,"a+")

    print("[*]["+getTime()+"] Logging to file %s" % log_file)
    log("[*]["+getTime()+"] Starting Scan against %s " % site)
    log("[*]["+getTime()+"] Verbose Mode On!")
    log("[*]["+getTime()+"] DNS Server Set to %s" % dns_server)
    log("[*]["+getTime()+"] Output to %s" % output_file)
    log("[*]["+getTime()+"] BEWARE: This may overwrite the file if it's already existing.")
    log("[*]["+getTime()+"] Using wordlist %s" % wordlist)
    log("[*]["+getTime()+"] Concurrency set to %s" % concurrent)
    log("[*]["+getTime()+"] Logging to file %s" % log_file)




#Delay the script from running to allow users to read options
if args.verbose:
    time.sleep(5)

resolver = dns.resolver.Resolver()
resolver.nameservers = [socket.gethostbyname(dns_server)]
resolver.timeout = 1
resolver.lifetime = 1


def doWork():
    while True:
        word = q.get()
        getStatus(word)
        q.task_done()
        if q.empty():
            #print("empty queue")
            pass


def warning():
    return "\033[1;31;40m[*]["+getTime()+"] "

def error():
    return "\033[0m 0;37;40m[*]["+getTime()+"] "

def info():
    return "\033[0;37;40m[*]["+getTime()+"] "

def success():
    return"\033[1;32;40m[*]["+getTime()+"] "



def getStatus(domain):
    try:
        answers = dns.resolver.query(domain)
        #for rdata in answers: # for each response
            #print("Resolved " + domain + " : " +str(rdata)) # print the data
        appenddataset1(domain)
        if args.verbose:  
            print(success()+"Resolved domain %s" % domain)
        else:
            print(domain)
        log("Resolved domain %s" % domain)
        out_file.write(domain+"\n")
    except dns.resolver.Timeout:
        if args.verbose:  
            print(warning()+"Timeout for domain %s" % domain)        
        addbacktoqueue(domain)
        log("Timeout for domain %s" % domain)      
        
    except dns.resolver.NXDOMAIN:
        if args.verbose:
            print(info()+"No such domain %s" % domain)
        log("No such domain %s" % domain)
        pass
    except dns.resolver.NoAnswer:
        if args.verbose:        
            print(success()+"Not resolved %s" % domain)
        appenddataset1(domain)
        log("Not resolved %s" % domain)
    except dns.exception.DNSException:
        #print("Unhandled exception")
        log("Not resolved %s" % domain)
        pass


def appenddataset():
    try:
        for words in open(wordlist ,'r'):
            q.put(words.strip() + "." + site)
        q.join()    
    except exception as e:
        print(e)
        log(e)



def appenddataset1(domain):
    try:
        for words in open(wordlist ,'r'):
            q.put(words.strip() + "." + domain)
    except exception as e:
        print(e)
        log(e)
        

def addbacktoqueue(domain):
    q.put(domain)



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


appenddataset()

out_file.close()
logfile.close()
