from django.shortcuts import render
from django.http import HttpResponse
from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet,Nalog,Semestar,Student


def timetableforuser(request,username):
    nalog = Nalog.objects.get(username=username)
    student = Student.objects.get(nalog=nalog)
    grupa = Student.objects.get(grupa = student.grupa)
    termini = []
    termini.append(Termin.objects.get(grupe=grupa))
    return HttpResponse(termini)


