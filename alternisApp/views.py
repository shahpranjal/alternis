import json
from django.http import HttpResponse
from django.shortcuts import render
from alternisApp.lib.queryapi import google_query,bing_query, correction_query
from alternisApp.lib.queryform import QueryForm


# Main Page
def index(request):
    form = QueryForm()
    return render(request, 'alternis/index.html', {'form': form})

# Return Query Results

def query(request):
    q = request.GET.get('q','')
    form = QueryForm()
    google_results = google_query(q)
    bing_results = bing_query(q)
    results_list = list(set().union(*[google_results,bing_results]))
    return render(request, 'alternis/results.html', { 'form': form, 'q': q, 'gr': results_list})
