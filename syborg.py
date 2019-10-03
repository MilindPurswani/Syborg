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

if args.wordlist:
    wordlist = args.wordlist
else:
    wordlist = "wordlist.txt"

if args.concurrency:
    concurrent = args.concurrency
else:
    concurrent = 10


if args.verbose:
    print("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] Starting Scan against %s " % site)
    print("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] Verbose Mode On!")
    print("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] DNS Server Set to %s" % dns_server)
    print("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] Output to %s" % output_file)
    print("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] BEWARE: This may overwrite the file if it's already existing.")
    print("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] Using wordlist %s" % wordlist)
    print("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] Concurrency set to %s" % concurrent)

def log(data):
    logfile = open(log_file,"a+")
    logfile.write(data+"\n")

    logfile.close()

if args.enablelogging:
    log_file = output_file+"-"+"log.log"
    print("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] Logging to file %s" % log_file)
    log("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] Starting Scan against %s " % site)
    log("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] Verbose Mode On!")
    log("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] DNS Server Set to %s" % dns_server)
    log("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] Output to %s" % output_file)
    log("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] BEWARE: This may overwrite the file if it's already existing.")
    log("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] Using wordlist %s" % wordlist)
    log("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] Concurrency set to %s" % concurrent)
    log("[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] Logging to file %s" % log_file)




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
    return "\033[1;31;40m[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] "

def error():
    return "\033[0m 0;37;40m[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] "

def info():
    return "\033[0;37;40m[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] "

def success():
    return"\033[1;32;40m[*]["+time.strftime("%Y:%m:%d - %H:%M:%S")+"] "

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
        if args.enablelogging:
            log("Resolved domain %s" % domain)
        file = open(output_file,"a")
        file.write(domain+"\n")
        file.close() 
    except dns.resolver.Timeout:
        if args.verbose:  
            print(warning()+"Timeout for domain %s" % domain)        
        addbacktoqueue(domain)
        if args.enablelogging:
            log("Timeout for domain %s" % domain)      
        pass
    except dns.resolver.NXDOMAIN:
        if args.verbose:
            print(info()+"No such domain %s" % domain)
        if args.enablelogging:
            log("No such domain %s" % domain)
        pass
    except dns.resolver.NoAnswer:
        if args.verbose:        
            print(success()+"Not resolved %s" % domain)
        appenddataset1(domain)
        if args.enablelogging:
            log("Not resolved %s" % domain)
    except dns.exception.DNSException:
        #print("Unhandled exception")
        if args.enablelogging:
            log("Not resolved %s" % domain)
        pass


def appenddataset():
    try:
        for words in open(wordlist ,'r'):
            q.put(words.strip() + "." + site)
        q.join()    
    except exception as e:
        print(e)
        if args.enablelogging:
            log(e)



def appenddataset1(domain):
    try:
        for words in open(wordlist ,'r'):
            q.put(words.strip() + "." + domain)
    except exception as e:
        print(e)
        if args.enablelogging:
            log(e)
        
failed_dict = {}

def addbacktoqueue(domain):
    if domain in failed_dict:
        if failed_dict[domain] >= threshold:
            if args.enablelogging:
                log("Not putting %s into queue[Failed attempts exceeded]" % domain)
            print("Not putting %s into queue[Failed attempts exceeded]" % domain)
        else:
            failed_dict[domain] += 1
            q.put(domain)
    else:
        failed_dict[domain] = 1
        q.put(domain)



q = filequeue.FileQueue(maxsize=1000)
try:
    file = open(output_file,"w+")
except exception as e:
    print(e)
    if args.enablelogging:
        log(e)    
    exit(1)


for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()


appenddataset()