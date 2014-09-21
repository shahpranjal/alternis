import urllib2
import xml.etree.ElementTree as ET
import json

# Query Google API
def google_query(Search):
    search_str = Search.replace(' ', '+') + '+vs'
    url = 'http://google.com/complete/search?output=toolbar&q=' + search_str
    serialized_data = urllib2.urlopen(url).read()
    tree = ET.fromstring(serialized_data)
    competitor = []
    if tree:
        for rivals in tree:
            rawData = str(rivals[0].attrib['data'])
            if ' vs ' in rawData:
                competitor = list(set().union(*[competitor, extract_vs(rawData)]))
    return competitor

# Query Bing API
def bing_query(Search):
    search_str = Search.replace(' ', '+') + '+vs'
    url = 'http://api.bing.com/osjson.aspx?query=' + search_str
    jsonval=json.loads(urllib2.urlopen(url).read())
    competitor= []
    if jsonval:
        for rivals in jsonval[1]:
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
    key = "AIzaSyDRuRGJMcgzKKQab30I6wo3LPClH8zCrkQ"
    cx = "009266886036344981856:9v3ra3nikya"
    url = "https://www.googleapis.com/customsearch/v1?searchType=image&key=%s&cx=%s&q=%s+logo" % (key, cx, query)
    jsonVal= json.loads(urllib2.urlopen(url).read())
    if not (jsonVal and "items" in jsonVal and "link" in jsonVal["items"][0]):
        return None
    return jsonVal["items"][0]["link"]

#Get wikipedia information
def wiki_query(query):
    query= query.replace(' ', '+')
    query= query.replace(',', '|')
    url = 'http://en.wikipedia.org/w/api.php?format=json&action=query&titles=Xbox%20360&prop=revisions&rvprop=content' + query
    jsonVal= json.loads(urllib2.urlopen(url).read())
    if (jsonVal):
        for page in jsonVal[0][1]:
            if "rivisions" in page:
                page_info = page["revisions"]
    return page_info



# Split string on vs
def extract_vs(str):
    return str.split(' vs ')

