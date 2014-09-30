import json
from django.http import HttpResponse
from django.shortcuts import render
from alternisApp.lib.queryapi import get_results
from alternisApp.lib.queryform import QueryForm


# Main Page
def index(request):
    form = QueryForm()
    return render(request, 'alternis/index.html', {'form': form})

# Return Query Results

def query(request):
    q = request.GET.get('q','')
    form = QueryForm(initial={'q': q})
    results_list = get_results(q)
    return render(request, 'alternis/results.html', { 'form': form, 'q': q, 'gr': results_list})