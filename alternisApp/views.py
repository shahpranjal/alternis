import json
from django.http import HttpResponse
from alternisApp.lib.queryapi import google_query,bing_query,correction_query
from django.shortcuts import render
from alternisApp.lib.queryapi import google_query,bing_query


# Main Page
def index(request):
    return render(request, 'alternis/index.html')


# Return Query Results
def query(request, Search):
    # t = loader.get_template('query.html')
    # c = Context({
    #
    # })
    #return HttpResponse(t.render(c))
    firstSearchResult = correction_query(Search)
    setUnion = list(set().union(*[google_query(Search),bing_query(Search)]))
    if (Search.upper().replace(' ', '') == firstSearchResult.upper().replace(' ','')):
        return HttpResponse(json.dumps(setUnion))
    return HttpResponse('Correction ' + firstSearchResult)

