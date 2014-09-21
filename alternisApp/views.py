import json
from django.http import HttpResponse
from alternisApp.lib.queryapi import google_query,bing_query,correction_query
from django.shortcuts import render
from alternisApp.lib.queryapi import google_query,bing_query
from alternisApp.lib.queryform import QueryForm


# Main Page
def index(request):
    form = QueryForm()
    return render(request, 'alternis/index.html', {'form': form})

# Return Query Results

def query(request):
    q = request.GET.get('q','')
    google_results = google_query(q)
    bing_results = bing_query(q)
    results_list = list(set().union(*[google_results,bing_results]))
    return render(request, 'alternis/results.html', { 'q': q, 'gr': results_list})

def query(request, Search):
    # t = loader.get_template('query.html')
    # c = Context({
    #
    # })
    #return HttpResponse(t.render(c))
    firstSearchResult = ''.join(correction_query(Search))
    setUnion = list(set().union(*[google_query(Search),bing_query(Search)]))
    if Search.upper().replace(' ', '') == firstSearchResult.upper().replace(' ',''):
        return HttpResponse(json.dumps(setUnion))
    #return HttpResponse(json.dumps(setUnion))
    return HttpResponse('Correction ' + firstSearchResult)

