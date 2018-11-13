from django.shortcuts import render
from django.http import HttpResponse
from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet, Nalog, Semestar, Student,Obavestenje
import datetime



def timetableforuser(request, username):
    nalog = Nalog.objects.get(username=username)
    resp = "<html><head><meta charset=\"UTF-8\"></head><body>"

    print(nalog.username + ' ' + nalog.uloga)


    if nalog.uloga == 'student':
        student = Student.objects.get(nalog=nalog)
        grupa = Grupa.objects.filter(student__id = student.id)
        termini = Termin.objects.filter(grupe__id=grupa[0].id)


        for termin in termini:
            resp += "<p>"
            resp += termin.dan + " "
            resp += termin.pocetak.strftime("%H:%M") + " "
            resp += termin.zavrsetak.strftime("%H:%M") + " "
            resp += termin.predmet.naziv + " "
            resp += "<span style=\"float:right\">" + termin.nastavnik.ime + " " + termin.nastavnik.prezime + "</span>"
            resp += termin.tip_nastave + " "
            resp += "</p>"
    elif nalog.uloga == 'nastavnik':
        nastavnik = Nastavnik.objects.get(nalog=nalog)
        termini = Termin.objects.filter(nastavnik__id=nastavnik.id)

        for termin in termini:
            resp += "<p>"
            resp += termin.dan + " "
            resp += termin.pocetak.strftime("%H:%M") + " "
            resp += termin.zavrsetak.strftime("%H:%M") + " "
            resp += termin.predmet.naziv + " "
            resp += "<span style=\"float:right\">" + termin.nastavnik.ime + " " + termin.nastavnik.prezime + "</span>"
            resp += termin.tip_nastave + " "
            resp += "</p>"
    else:
        resp += '<p>No result</p>'

    resp += "</body></html>"

    return HttpResponse(resp)

def nastavnici_template(request):
    qs = Nastavnik.objects.all()
    context = {'nastavnici': qs }
    return render(request,'studserviceapp/nastavnici.html', context)

def unos_obavestenja_form(request,user):
    try:
        n = Nalog.objects.get(username = user)
        # if n.uloga=='sekretar' or n.uloga=='administrator':
        context = {'nalog':n}
        return render(request, 'studserviceapp/unosobavestenja.html',context)
        # else:
        #     return HttpResponse('<h1>Korisnik mora biti sekretar ili administrator</h1>')
    except Nalog.DoesNotExist:
        return HttpResponse('<h1>Username '+ user+' not found</h1>')

def save_obavestenje(request):
    # tekst = request.POST['tekst']
    # postavio = Nalog.objects.get(username=request.POST['postavio'])
    # obavestenje = Obavestenje(tekst=tekst,postavio=postavio,datum_postavljanja=datetime.datetime.now())
    # obavestenje.save()
    return HttpResponse("<h1>Uspesno savcuvano obavestenje</h1>")

def unos_semestra_form(request,user):
    try:
        n = Nalog.objects.get(username = user)
        p = Predmet.objects.all()
        context = {'predmeti':p}
        return render(request, 'studserviceapp/unossemestra.html', context)
    except Predmet.DoesNotExist:
        return HttpResponse("<h1> Nema predmeta u bazi</h1>")

def save_semestra(request):
    return HttpResponse("<h1>Uspesno savcuvan semestar</h1>")


