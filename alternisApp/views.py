import json
from django.http import HttpResponse
from alternisApp.lib.queryapi import google_query,bing_query

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

    return HttpResponse(json.dumps(list(set().union(*[google_query(Search),bing_query(Search)]))))
