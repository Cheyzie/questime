from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

# Create your views here.
def index(request):
    return HttpResponse("{'name':'Classtime','action':'Suck'}")