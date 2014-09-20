import json
from django.http import HttpResponse
from alternisApp.lib.queryapi import google_query,bing_query,correction_query

# Main Page
def index(request):
    return HttpResponse("Hello, search for alternatives please")


# Return Query Results
def query(request, Search):
    # t = loader.get_template('query.html')
    # c = Context({
    #
    # })
    #return HttpResponse(t.render(c))
    firstSearchResult = correction_query(Search)
    setUnion = list(set().union(*[google_query(Search),bing_query(Search)]))
    #return  HttpResponse(Search.upper().strip() + " - " + firstSearchResult.upper().strip())
    if (Search.upper().replace(' ', '') == firstSearchResult.upper().replace(' ','')):
        return HttpResponse(json.dumps(setUnion))
    return HttpResponse('Correction ' + firstSearchResult)

