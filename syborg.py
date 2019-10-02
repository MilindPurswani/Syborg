from threading import Thread
import sys
from filequeue import *
import sys
import socket
import dns.resolver
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("domain",help="domain name of the target")
parser.add_argument("dns",help="dns of the target")
parser.add_argument("output_file",help="Output file path")
parser.add_argument("-v", "--verbose", help="increase output verbosity",action="store_true")
args = parser.parse_args()
if args.verbose:
    print("[*] Verbose Mode On!")
site = args.domain
dns_server = args.dns
output_file = args.output_file

resolver = dns.resolver.Resolver()
resolver.nameservers = [socket.gethostbyname(dns_server)]
resolver.timeout = 1
resolver.lifetime = 1

concurrent = 50

def doWork():
    while True:
        word = q.get()
        #print(word)
        domain = getStatus(word)
        q.task_done()
        if q.empty():
            #print("empty queue")
            pass



def getStatus(domain):
    #domain = word + "." + site
    #print("Checking for domain " + domain)
    try:
        answers = dns.resolver.query(domain)
        #for rdata in answers: # for each response
            #print("Resolved " + domain + " : " +str(rdata)) # print the data
        appenddataset1(domain)
        print(domain)
        file = open(output_file,"a")
        file.write(domain+"\n")
        file.close() 
    except dns.resolver.Timeout:
        if args.verbose:  
            print("[*] Timeout for domain %s" % domain)        
        addbacktoqueue(domain)
        pass
    except dns.resolver.NXDOMAIN:
        if args.verbose:
            print("[*] No such domain %s" % domain)
        pass
    except dns.resolver.Timeout:
        if args.verbose:
            print("[*] Timed out while resolving %s" % domain)
        pass
    except dns.resolver.NoAnswer:
        if args.verbose:        
            print("[*] Not resolved %s" % domain)
        appenddataset1(domain)
    except dns.exception.DNSException:
        #print("Unhandled exception")
        pass
    return "1"

def appenddataset():
    try:
        for words in open('wordlist.txt' ,'r'):
            #print("Adding data to queue : " + words.strip() + "." + site)
            q.put(words.strip() + "." + site)
        q.join()    
        #print("Data added to queue")
    except exception as e:
        print(e)



def appenddataset1(domain):
    try:
        for words in open('wordlist.txt' ,'r'):
            #print("Adding data to queue : " + words.strip() + "." + domain)
            q.put(words.strip() + "." + domain)
        #aq.join()
        #print("Data added to queue")
    except exception as e:
        print(e)
def addbacktoqueue(domain):
    q.put(domain)

def doSomethingWithResult():
    pass


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


