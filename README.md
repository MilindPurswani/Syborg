# Syborg
Syborg is a Recursive DNS Domain Enumerator which is neither active nor completely passive. This tool simply constructs a domain name and queries it with a specified DNS Server.

![carbon.png](carbon.png)
Image Credits: [Carbon](https://carbon.now.sh)

Syborg has a Dead-end Avoidance system inspired from [@Tomnomnom](https://github.com/tomnomnom/hacks)'s [ettu](https://github.com/tomnomnom/hacks). 

When you run subdomain enumeration with some of the tools, most of them passively query public records like `virustotal`, `crtsh` or `censys`. This enumeration technique is really fast and helps to find out a lot of domains in much less time.

However, there are some domains that may not be mentioned in these public records. Inorder to find those domains, Syborg interacts with the nameservers and recursively brute-forces subdomain from the DNS until it's queue is empty. 

As mentioned by[@Tomnomnom](https://github.com/tomnomnom/hacks)'s [ettu](https://github.com/tomnomnom/hacks), I quote:

> Ordinarily if there are no records to return for a DNS name you might expect an `NXDOMAIN` error:
> ```bash
> ▶ host four.tomnomnom.uk
> Host four.tomnomnom.uk not found: 3(NXDOMAIN)
> ```
> You may have noticed that sometimes you get an empty response instead though:
> ```bash
> ▶ host three.tomnomnom.uk
> ```
> The difference in the latter case is often that another name - one that has your queried name as a suffix - exists and has records to return
> ```bash
> ▶ host one.two.three.tomnomnom.uk
> one.two.three.tomnomnom.uk has address 46.101.59.42
> ```
> This difference in response can be used to help avoid dead-ends in recursive DNS brute-forcing by not recusing in the former situation:
> ```bash
> ▶ echo -e "www\none\ntwo\nthree" | ettu tomnomnom.uk
> one.two.three.tomnomnom.uk
> ```

Syborg incorporates all of these functionalities with simple concurrency and recursion.

## Requirements:

Python 3.x (Recommended)

Python 2.x (Not tested)

## Installation:

Clone the repo using the `git clone` command as follows:

```bash
git clone https://github.com/MilindPurswani/Syborg.git
```

Resolve the Dependencies:

```bash
pip3 install -r requirements.txt
```

## Usage:

```bash
python3 syborg.py yahoo.com 
```


## Using Smartly:

1. By default this will use the built-in wordlist (Courtesy: [altdns](https://github.com/infosec-au/altdns)) which may or may not generate appropriate results. If you are looking for a good wordlist, I suggest you use [@tomnomnom](https://github.com/tomnomnom) `assetfinder` and `tok` tool to generate a domain specific word-list. 

```bash
assetfinder --subs-only media.yahoo.com | tok | sort -u -delim-exceptions=- | tee -a media.yahoo.com-wordlist.txt
```

2. At times, it is possible that Syborg will hit High CPU Usage and that can cost you a lot if you are trying to use this tool on your VPS. Inorder to limit that use another utility called cpulimit

```bash
cpulimit -l 50 -p $(pgrep python3)
```

This tool can be downloaded as follows:

```bash
sudo apt install cpulimit
```

For more help regarding usage, 

```bash
python3 syborg.py -h
```
