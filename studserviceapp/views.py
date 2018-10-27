from django.shortcuts import render
from django.http import HttpResponse
from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet,Nalog,Semestar,Student

import time


def timetableforuser(request,username):
    nalog = Nalog.objects.get(username=username)
    student = Student.objects.get(nalog=nalog)

    grupa = Grupa.objects.filter(student__id = student.id)

    termini = []
    termini = Termin.objects.filter(grupe__id = grupa[0].id)

    resp = "<html><head><meta charset=\"UTF-8\"></head><body>"

    for termin in termini:
        resp += "<p>"
        resp += termin.dan + " "
        resp += termin.pocetak.strftime("%H:%M") + " "
        resp += termin.zavrsetak.strftime("%H:%M") + " "
        resp += termin.predmet.naziv + " "
        resp += "<span style=\"float:right\">" + termin.nastavnik.ime + " " + termin.nastavnik.prezime + "</span>"
        resp += termin.tip_nastave + " "
        resp += "</p>"

    resp += "</body></html>"

    return HttpResponse(resp) 

