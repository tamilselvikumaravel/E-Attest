import urllib
import time
from collections import deque
import sys
def get_page(url):
    try:
        f = urllib.urlopen(url)
        page = f.read()
        #print "page",page
        f.close()
        return page
    except:
        return ""

def union(a,b):
    for e in b:
        if e not in a:
            a.append(e)

def get_next_url(page):
    start_link=page.find("<a href=")
    if start_link == -1:
        return None,0
    start_quote=page.find('"',start_link)
    end_quote = page.find('"',start_quote+1)
    url=page[start_quote+1:end_quote] 
    return url,end_quote

def get_all_links(page):
    link=[]
    while True:
        url,endpos=get_next_url(page)

        if url:
            link.append(url)
            page=page[endpos]
        else:
            break
    
    return link


def add_to_index(index,url,keyword):
    if keyword in index:
        if not url in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword] = [url]
    #print "index",index
    return index

def split_string(source,splitlist):
	return ''.join([w if w not in splitlist else ' ' for w in source]).split()

def add_page_to_index(index,url,content):
    words = split_string(content,"_!")
    #print"words:",words
    for word in words:
        add_to_index(index,url,word)
def crawl_web(seed,max_pages):
 start = time.clock()
 tocrawl=deque(seed)
 crawled =[]
 index ={}
 graph={}
 
 depth=0
 while tocrawl:
    page=tocrawl.popleft()
    #print "page",page
    if max_pages>0:
	  
             c=get_page(page)
             #print "depth",depth
             #print c
             add_page_to_index(index,page,c)
             f= get_all_links(c)
             #print f
             union(tocrawl, f)
             graph[page] = f
             crawled.append(page)
             max_pages=max_pages-1
 	     #print "hi"
 t1 = time.clock() - start
 #print "crawled",crawled
 return graph
def display_search():
 #n=int(raw_input("enter number of urls:"))
 #seed_page=[]
 #ss=[]
 ss=sys.stdin
 #ss=seed_page.split(" ")
 #print ss
 max_pages = 6
 
# print seed_page
 #for i in range(len(ss)):
 #crawled,index,graph, t1 = crawl_web(ss,max_pages)
 graph=crawl_web(ss,max_pages)
 #print graph
 for i in graph:
     print i, 1

 #print 'https://support.google.com/accounts/answer/61416 1'
 #ranks,t2 = compute_ranks(graph)
 #print "crawl_time",t1
	  #print "index",index
 #print "index len: ",len(index)
 #print "graph len: ", len(graph)
	  #print "index", index
	  #print "graph", graph
 #print "rank_time",t2
 #print "ranks: ", ranks
 #key=raw_input('enter keyword:')
 #print "lookup",Look_up(index,key)
	  #print "best_page",best_search(index,ranks,"Computer")
 #vv(index,ranks)
   #n=raw_input("enter number:")
      #print "reverse:"reverse(n)  
if __name__ == "__main__":
	  display_search()
