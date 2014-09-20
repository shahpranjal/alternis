from django.http import HttpResponse
from django.db.migrations import loader
import urllib2
import xml.etree.ElementTree as ET
import json

def index(request):
    return HttpResponse("Hello, search for alternatives please")

def query(request, Search):
    # t = loader.get_template('query.html')
    # c = Context({
    #
    # })
    #return HttpResponse(t.render(c))
    url = 'http://google.com/complete/search?output=toolbar&q=' + Search + '+vs'
    serialized_data = urllib2.urlopen(url).read()
    tree = ET.fromstring(serialized_data)
    competitor = []
    if (tree):
        for rivals in tree:
            rawData = (rivals[0].attrib['data'])
            if ('vs' in rawData):
                indexOf = rawData.find('vs')
                competitor.append(rawData[indexOf+2:])
    else:
        return  HttpResponse("err")
    return HttpResponse(json.dumps(competitor) + ' ' + url)
