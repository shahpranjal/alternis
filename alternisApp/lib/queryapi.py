import urllib2
import xml.etree.ElementTree as ET
import json

# Query Google API
def google_query(Search):
    search_str = Search + '+vs'
    url = 'http://google.com/complete/search?output=toolbar&q=' + search_str
    serialized_data = urllib2.urlopen(url).read()
    tree = ET.fromstring(serialized_data)
    competitor = []
    if (tree):
        for rivals in tree:
            rawData = (rivals[0].attrib['data'])
            if ('vs' in rawData):
                indexOf = rawData.find('vs')
                if (rawData[indexOf+2:] != ''):
                    competitor.append(rawData[indexOf+2:])
    return competitor

# Query Bing API
def bing_query(Search):
    search_str = Search + '+vs'
    competitor = []
    url = 'http://api.bing.com/osjson.aspx?query=' + search_str
    jsonVal= json.loads(urllib2.urlopen(url).read())
    if (jsonVal):
        for rivals in jsonVal[1]:
            if ('vs' in rivals):
                indexOf = rivals.find('vs')
                competitor.append(rivals[indexOf+2:])
    return competitor

#DidYouMean?
def correction_query(Search):
    url = 'http://suggestqueries.google.com/complete/search?output=toolbar&hl=en&q=' + Search + '&gl=us'
    serialized_data = urllib2.urlopen(url).read()
    tree = ET.fromstring(serialized_data)
    if (tree):
        return tree[0][0].attrib['data']
    return 'Could not find any suggestions'