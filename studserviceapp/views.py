from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Mrs")

def timetableforuser(request,username):
    return HttpResponse("Dobrodošli na studentski servis, raspored za username %s." % username)


