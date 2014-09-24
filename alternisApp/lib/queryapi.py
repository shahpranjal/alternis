import urllib2
import xml.etree.ElementTree as ET
import json
import tfidf as tf
import unicodedata



# Query Google API
def google_query(Search):
    search_str = Search.replace(' ', '+') + '+vs'
    url = 'http://google.com/complete/search?output=toolbar&q=' + search_str
    serialized_data = urllib2.urlopen(url).read()
    tree = ET.fromstring(serialized_data)
    competitor = []
    if (tree):
        for rivals in tree:
            rawData = str(rivals[0].attrib['data'])
            if ' vs ' in rawData:
                competitor = list(set().union(*[competitor, extract_vs(rawData)]))
    return competitor

# Query Bing API
def bing_query(Search):
    search_str = Search.replace(' ', '+') + '+vs'
    url = 'http://api.bing.com/osjson.aspx?query=' + search_str
    jsonVal= json.loads(urllib2.urlopen(url).read())
    competitor= []
    if (jsonVal):
        for rivals in jsonVal[1]:
            if ' vs ' in rivals:
                competitor = list(set().union(*[competitor, extract_vs(str(rivals))]))
    return competitor

#DidYouMean?
def correction_query(Search):
    url = 'http://suggestqueries.google.com/complete/search?output=toolbar&hl=en&q=' + Search.replace(' ', '+') + '&gl=us'
    serialized_data = urllib2.urlopen(url).read()
    tree = ET.fromstring(serialized_data)
    if (tree):
        return tree[0][0].attrib['data'].split(' ')
    return 'Could not find any suggestions'

#Image Search
def google_image_search(query):
    query = query.replace(' ', '+')

    key = "AIzaSyA9a4pR6mLrql8NUO-E-Er9YJhxZOlcuco"
    cx = '017102084845186701248:-ou89komm5s'
    url = "https://www.googleapis.com/customsearch/v1?searchType=image&key=%s&cx=%s&q=%s+logo" % (key, cx, query)
    jsonVal= json.loads(urllib2.urlopen(url).read())
    if not (jsonVal and "items" in jsonVal and "link" in jsonVal["items"][0]):
        return None
    return str(jsonVal["items"][0]["link"])


#Google Desc + URL Search
def google_url_search(query):
    query = query.replace(' ', '+')
    key = "AIzaSyA9a4pR6mLrql8NUO-E-Er9YJhxZOlcuco"
    cx = '017102084845186701248:-ou89komm5s'
    url = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s" % (key, cx, query)
    jsonVal= json.loads(urllib2.urlopen(url).read())
    if not (jsonVal and "items" in jsonVal and "link" in jsonVal["items"][0]):
        return None
    link = jsonVal["items"][0]["link"]
    snippet = jsonVal["items"][0]["snippet"]
    return {'desc':snippet.encode('ascii','ignore'),'url':link.encode('ascii','encode')}


#DuckDuckGo
def duckduckgo_search(query):
    query = query.replace(' ','')
    url = 'http://api.duckduckgo.com/?q=' + query + '&format=json'
    site_url = ''
    abstract = ''
    jsonVal= json.loads(urllib2.urlopen(url).read())
    if 'Abstract' in jsonVal:
        abstract = jsonVal['Abstract']
    if 'Results' in jsonVal:
        if 'FirstURL' in jsonVal['Results']:
            site_url = str(jsonVal['Results'][0]['FirstURL'])
    return {'desc':str(abstract),'url':str(site_url)}


#Get wikipedia information
def wiki_query(query):
    query= query.replace(' ', '+')
    query= query.replace(',', '|')
    page_info = ''
    url = 'http://en.wikipedia.org/w/api.php?format=json&action=query&titles=' + query + '&prop=revisions&rvprop=content'
    jsonVal= json.loads(urllib2.urlopen(url).read())
    if (jsonVal):
        for page in jsonVal["query"]["pages"]:
            i = jsonVal["query"]["pages"][page]
            if "revisions" in i:
                page_info = i["revisions"]
    tfobj = tf.TfIdf()
    input_doc = tfobj.add_input_document(str(page_info))
    keywords = tfobj.get_idf(str(query))
    return keywords
    return page_info

# data to send to view
def get_results(q):
    searched_item = get_searched_item(q)
    google_results = google_query(q)
    bing_results = bing_query(q)
    set__union = set().union(*[google_results, bing_results])
    set__union.discard(searched_item)
    results_list = list(set__union)
    sorted_list= sorted(results_list,key=len)
    sorted_list.insert(0, searched_item)
    sorted_list = normalize(sorted_list)
    sorted_list.discard(searched_item)
    results_list = list(sorted_list)
    results_list.insert(0, searched_item)
    ret = []
    for item in results_list:
        tmp = dict()
        duckresults = google_url_search(item)
        tmp["title"] = item
        tmp["link"] = duckresults["url"]
        tmp["desc"] = duckresults["desc"]
        #tmp["img"] = google_image_search(item)
        ret.append(tmp)
    return ret


# Try to normalize the data a little more
def normalize(q):
    results_to_eliminate = []
    for index1 in range(0, len(q)):
        for index2 in range(index1 + 1, len(q)):
            firstItem = str(q[index1])
            nextItem = str(q[index2])
            if firstItem.upper().replace(' ','') in nextItem.upper().replace(' ',''):
                results_to_eliminate.append(nextItem)
    return set(q) - set(results_to_eliminate)


# Get searched item
def get_searched_item(q):
    search_str = q.replace(' ', '+') + '+vs'
    url = 'http://api.bing.com/osjson.aspx?query=' + search_str
    jsonVal= json.loads(urllib2.urlopen(url).read())
    index_of_vs_in_search = jsonVal[0].find(" vs")
    return str(jsonVal[0][:index_of_vs_in_search])


# Split string on vs
def extract_vs(str):
    return str.split(' vs ')
