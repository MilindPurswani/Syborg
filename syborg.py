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
parser.add_argument("-v", "--verbose", help="increase output verbosity",action="store_true")
args = parser.parse_args()
if args.verbose:
    print("[*] Verbose Mode On!")
site = args.domain

if args.dns:
    dns_server = args.dns
else:
    dns_server = "8.8.8.8"

if args.verbose:
    print("[*] DNS Server Set to %s" % dns_server)

if args.output:
    output_file = args.output
else:
    output_file = "results-"+site+".txt"

if args.verbose:
    print("[*] Output to %s" % output_file)
    print("[*] BEWARE: This may overwrite the file if it's already existing.")


if args.wordlist:
    wordlist = args.wordlist
else:
    wordlist = "wordlist.txt"

if args.verbose:
    print("[*] Using wordlist %s" % wordlist)

if args.concurrency:
    concurrent = args.concurrency
else:
    concurrent = 10

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
    return "\033[1;31;40m [*] "

def error():
    return "\033[0m 0;37;40m [*] "

def info():
    return "\033[0;37;40m [*] "

def success():
    return"\033[1;32;40m [*] "

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
        file = open(output_file,"a")
        file.write(domain+"\n")
        file.close() 
    except dns.resolver.Timeout:
        if args.verbose:  
            print(warning()+"Timeout for domain %s" % domain)        
        addbacktoqueue(domain)
        pass
    except dns.resolver.NXDOMAIN:
        if args.verbose:
            print(info()+"No such domain %s" % domain)
        pass
    except dns.resolver.NoAnswer:
        if args.verbose:        
            print(success()+"Not resolved %s" % domain)
        appenddataset1(domain)
    except dns.exception.DNSException:
        #print("Unhandled exception")
        pass


def appenddataset():
    try:
        for words in open(wordlist ,'r'):
            q.put(words.strip() + "." + site)
        q.join()    
    except exception as e:
        print(e)



def appenddataset1(domain):
    try:
        for words in open(wordlist ,'r'):
            q.put(words.strip() + "." + domain)
    except exception as e:
        print(e)

def addbacktoqueue(domain):
    q.put(domain)



q = filequeue.FileQueue(maxsize=1000)
try:
    file = open(output_file,"w+")
except exception as e:
    print(e)
    exit(1)


for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()

appenddataset()


