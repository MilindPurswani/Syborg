# Syborg Creative Usage Guidelines

Syborg is a great tool for Subdomain enumeration. It's really smart and fast. But it's simply dumb! That sounds quite contrary. Doesn't it? 

**How can it be a great tool, smart and fast, yet dumb?**

The answer is really simple! Syborg relies brute-forcing DNS servers for proper response. It recursively searches for subdomains by brute-forcing. That's it! Nothing more! However the power of this tool depends on how one uses it!

The wordlist provided with Syborg has a very limited, general set of words that are normally available. This wordlist does with in most of the cases but can't give you the results you are expecting. We have to be smart with how we query for subdomains using syborg. 

Here I am enlisting a few ways in which you can guarantee good results with Syborg.

## Try doing passive reconnaissance first.

Syborg works wonderfully if you have a domain specific wordlist. All domains are different. For instance, 

```
mail.google.com 
docs.google.com 
photos.google.com
```

are valid subdomains related to `google.com` but these subdomains may not be valid in case of `yahoo.com` simply meaning that the wordlist of `google.com` has to be tweaked a little before using it against `yahoo.com` for subdomain enumeration. This is what I mean by domain specific wordlist. 

This functionality is offered by a lot of tools and there is no point re-inventing the wheel, therefore I recommend using some of the tools mentioned below

### AssetFinder with tok

If you are looking for Passive reconnaissance, assetfinder is a great tool! It's simply fast.. This tool is offered by [@tomnomnom](https://github.com/tomnomnom/) and can be easily used in conjunction with Syborg. In order to use this tool, you should have `go` installed and properly configured. So, generate a wordlist with assetfinder as follows:

```
assetfinder --subs-only media.yahoo.com | tok -delim-exceptions=- | sort -u | tee -a media.yahoo.com-wordlist.txt
```

Inorder to install `assetfinder` and `tok`

```
go get -u github.com/tomnomnom/assetfinder
go get -u github.com/tomnomnom/hacks/tok
```

This will generate a great wordlist for you and look for hidden domains.

### [Sublist3r](https://github.com/aboul3la/Sublist3r)

Let alone Sublist3r is also enough for generating a domain specific wordlist. If you have Sublist3r you can use the following commands to create one.

```
python sublist3r.py -d media.yahoo.com -o domains.txt
cat domains.txt | sed 's/[.]/\n/g' | sort -u | tee -a media.yahoo.com-wordlist.txt
```

There is no limit to number of tools that can be used here. One can also use any other tool such as masscan. In the end all that matters is that we need a good wordlist, that can be used here.

## Taking it to Next Level

There are certain cases where the current wordlist isn't simply enough or we may need some more permutations inorder to search for such domains.

Consider this example:

```
python sublist3r.py -d milindpurswani.com
```

results in following domains:

```
www.milindpurswani.com
log.milindpurswani.com
mail.milindpurswani.com
```

Well, this is not looking so good, but our community is filled with creative people who have solutions to these problems. 

In this [article](https://0xpatrik.com/subdomain-enumeration-smarter/), [Patrik Hudak](https://0xpatrik.com/subdomain-enumeration-smarter/) explains a smarter way of doing reconnaissance. He introduces us with his new tool, [`dnsgen`](https://pypi.org/project/dnsgen/). This tool generates a combination of domain names from the provided input. Combinations are created based on wordlist. Custom words are extracted per execution (as he mentions). For more information, check out his repo. By simply running.

```
dnsgen domains.txt -w media.yahoo.com-wordlist.txt
```

You will have generated many possible combinations of subdomains that can be queried with resolvers (as he mentions). Let's take it to another step and pass this data to Syborg.

```
dnsgen domains.txt -w media.yahoo.com-wordlist.txt | sed 's/[.]/\n/g' | sort -u | tee -a media.yahoo.com-extreem-wordlist.txt
```

This resultant wordlist would contain almost all possible combinations of words that would be specific to any subdomain for which it has been made. Let's pass it to Syborg as follows:

```
python syborg.py media.yahoo.com -w media.yahoo.com-extreem-wordlist.txt -c 50 -v
```

I hope now you have some clear understanding of Syborg's usage. Simply dumb, yet Smart!