from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def apiData(request):
    import requests
    return HttpResponse("Hello world!")