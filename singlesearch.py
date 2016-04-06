
from py2neo import Node, Relationship
from py2neo import authenticate,Graph
sgraph = Graph()
authenticate("localhost:7474","neo4j","tamil")
sgraph = Graph("http://localhost:7474/db/data/")
def get_page(ss):
	try:
		print"url:",ss
		import urllib
		f = urllib.urlopen(ss)
		page = f.read()
		
		print "page",page
		f.close()
		return page
	except:
		return "" 
		
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
	
"""def Look_up(index, keyword):
    
    if keyword in index:
		return index[keyword]
    else:
        return None
    return []"""
		
		
def add_to_index(index,url,keyword):
    if keyword in index:
        if not url in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword] = [url]
		#print "index",index
    return index
	
def split_string(source,splitlist):
    return ''.join([ w if w not in splitlist else ' ' for w in source]).split()

def add_page_to_index(index,url,content):
    words = split_string(content,"_!")
    #print"words:",words
    for word in words:
        add_to_index(index,url,word)
		
def union(a,b):
    for e in b:
        if e not in a:
            a.append(e)
			
def test1(t1):
    v1=Node("x3",crawl_time=t1)
    sgraph.create(v1)	
			
def test(graph):
    for page in graph:
        s2=Node("x1",sgraph=graph[page])
        sgraph.create(s2)
        s1=Node("x1",spage=page)
        sgraph.create(s1)
        s1_link_s2 = Relationship(s1,"link",s2)
        sgraph.create(s1_link_s2)
		
def example(ranks):
    for ran in ranks:
		t2=Node("x2",r=ranks[ran])
		sgraph.create(t2)
		t3=Node("x2",r1=ran)
		sgraph.create(t3)
		t3_Rank_t2=Relationship(t3,"Rank",t2)
		sgraph.create(t3_Rank_t2)			
			
def compute_ranks(graph):
	import time
	start = time.clock()
	d=0.8
	numloops=10
	ranks={}
	npages=len(graph)
	for page in graph:#www.google.com:0.25,www.yahoo.com:0.25
		ranks[page]=1.0/npages
	for i in range(0,numloops):
		newranks={}
		for page in graph:
			newrank=(1-d)/npages#0.05
			for node in graph:
				if page in graph[node]:
					newrank=newrank+ d*(ranks[node]/len(graph[node]))#0.000000004
			newranks[page]=newrank#www.google.com:0.00000004
		ranks=newranks
	t2= time.clock() - start
	return ranks,t2
		
	
def crawl_web(ss,max_pages):
	tocrawl=[ss]
	#print"tocrawl:",tocrawl
	crawled =[]
	index ={}
	graph={}
	import time
	start = time.clock()
	while tocrawl:
		page=tocrawl.pop()
		#print "page",page
		if page not in crawled and max_pages>0:
			c=get_page(page)
			print "C:",c
			#print "depth",depth
			#print c
			add_page_to_index(index,page,c)
			f= get_all_links(c)
			union(tocrawl, f)
			graph[page] = f
			crawled.append(page)
			max_pages=max_pages-1
	t1 = time.clock() - start
	print "crawled",crawled
	return crawled,index,graph,t1
	
def display_search(ss):
	#if request.method=='POST':
		ss=ss
		#ss=request.form['ss']
		#ss=seed.split(" ")
		#max_pages=int(request.form['max_pages'])
		#max_pages=2
		max_pages=2
		#key=request.form['key']
		#key=key
		crawled,index,graph,t1=crawl_web(ss,max_pages)
		ranks,t2 = compute_ranks(graph)
		example(ranks)
		test(graph)
		test1(t1)
		print "crawl_time",t1
		length=len(index)
		print "index len: ",length
		print "rank_time",t2
		print "ranks: ", ranks
		print "graph is", graph
		m=len(graph)
		print "The graph length is",m
		#key=Look_up(index,key)
		#print "lookup",key
		return crawled,t1,length,t2,ranks,graph,m
		#print "best_page",best_search(index,ranks,"Computer")
		#vv(index,ranks)
		#return render_template('pg.html',crawled=crawled,t1=t1,length=length,rank_time=t2,ranks=ranks,key=key,graph=graph,graph_len=m)
		
	    
if __name__ == '__main__':
	display_search()



