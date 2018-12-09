from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet, Nalog, Semestar, Student, \
    Obavestenje, IzborGrupe, IzbornaGrupa
import datetime

# TODO BUG ovde
# from parser import import_timetable_from_csv


def timetableforuser(request, username):
    nalog = Nalog.objects.get(username=username)
    resp = "<html><head><meta charset=\"UTF-8\"></head><body>"

    print(nalog.username + ' ' + nalog.uloga)

    if nalog.uloga == 'student':
        student = Student.objects.get(nalog=nalog)
        grupa = Grupa.objects.filter(student__id=student.id)
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
    context = {'nastavnici': qs}
    return render(request, 'studserviceapp/nastavnici.html', context)


def unos_obavestenja_form(request, user):
    try:
        n = Nalog.objects.get(username=user)
        # if n.uloga=='sekretar' or n.uloga=='administrator':
        context = {'nalog': n}
        return render(request, 'studserviceapp/unosobavestenja.html', context)
        # else:
        #     return HttpResponse('<h1>Korisnik mora biti sekretar ili administrator</h1>')
    except Nalog.DoesNotExist:
        return HttpResponse('<h1>Username ' + user + ' not found</h1>')


def save_obavestenje(request):
    tekst = request.POST['tekst']
    postavio = Nalog.objects.get(username=request.POST['postavio'])
    fajl_obavestenje = request.FILES('fajl_obavestenje')
    obavestenje = Obavestenje(tekst=tekst, postavio=postavio, fajl=fajl_obavestenje,
                              datum_postavljanja=datetime.datetime.now())
    obavestenje.save()
    return HttpResponse("<h1>Uspesno sacuvano obavestenje</h1>")


def unos_semestra_form(request, user):
    try:
        n = Nalog.objects.get(username=user)
        p = Predmet.objects.all()
        context = {'predmeti': p}
        return render(request, 'studserviceapp/unossemestra.html', context)
    except Predmet.DoesNotExist:
        return HttpResponse("<h1> Nema predmeta u bazi</h1>")


def save_semestra(request):
    skolska_godina_pocetak = request.POST['skolska_godina_pocetak']
    skolska_godina_kraj = request.POST['skolska_godina_kraj']
    vrsta_semestra = request.POST['vrsta_semestra']
    oznaka_grupe = request.POST['oznaka_grupe']
    oznaka_semestra = request.POST['oznaka_semestra']
    kapacitet = request.POST['kapacitet']
    smer = request.POST['smer']
    if (request.POST['aktivnost'] == "aktivna"):
        aktivnost = True
    else:
        if (request.POST['aktivnost'] == "neaktivna"):
            aktivnost = False

    # print(skolska_godina_pocetak,skolska_godina_kraj,vrsta_semestra,oznaka_grupe,
    #       oznaka_semestra,kapacitet,smer,aktivnost)

    if (Semestar.objects.filter(vrsta=vrsta_semestra,
                                skolska_godina_pocetak=skolska_godina_pocetak,
                                skolska_godina_kraj=skolska_godina_kraj)):
        semestar = Semestar.objects.get(vrsta=vrsta_semestra,
                                        skolska_godina_pocetak=skolska_godina_pocetak,
                                        skolska_godina_kraj=skolska_godina_kraj)
    else:
        semestar = Semestar()
        semestar.vrsta = vrsta_semestra
        semestar.skolska_godina_pocetak = skolska_godina_pocetak
        semestar.skolska_godina_kraj = skolska_godina_kraj
        semestar.save()

    if (IzbornaGrupa.objects.filter(oznaka_grupe=oznaka_grupe, oznaka_semestra=oznaka_semestra)):
        return HttpResponse("<h1>Izborna grupa vec postoji</h1>")
    else:
        izbornaGrupa = IzbornaGrupa()
        izbornaGrupa.oznaka_grupe = oznaka_grupe
        izbornaGrupa.oznaka_semestra = int(oznaka_semestra)
        izbornaGrupa.kapacitet = int(kapacitet)
        izbornaGrupa.smer = smer
        izbornaGrupa.aktivna = aktivnost
        izbornaGrupa.za_semestar = semestar
        izbornaGrupa.save()

    predmeti = request.POST.getlist('predmeti')

    for p in predmeti:
        predmet = Predmet.objects.get(naziv=p)
        izbornaGrupa.predmeti.add(predmet)

    return HttpResponse("<h1>Uspesno sacuvan semestar</h1>")


def izmena_izborne_grupa_form(request, oznakaGrupe, vrstaSemestra):
    try:
        grupa = IzbornaGrupa.objects.get(oznaka_grupe=oznakaGrupe, za_semestar__vrsta=vrstaSemestra)
        predmeti = grupa.predmeti.all()
        context = {
            'grupa': grupa,
            'predmeti': predmeti
        }
        return render(request, 'studserviceapp/izmenaIzborneGrupe.html', context)
    except IzbornaGrupa.DoesNotExist:
        return HttpResponse('<h1>Ne postoji trazena izborna grupa')


def save_izmene_izborne_grupe(request):
    oznaka_grupe = request.POST['oznaka_grupe']
    oznaka_semestra = request.POST['oznaka_semestra']
    kapacitet = request.POST['kapacitet']
    if (request.POST['aktivnost'] == "aktivna"):
        aktivnost = True
    else:
        if (request.POST['aktivnost'] == "neaktivna"):
            aktivnost = False

    izbornaGrupa = IzbornaGrupa.objects.get(oznaka_grupe=oznaka_grupe,
                                            oznaka_semestra=oznaka_semestra)

    izbornaGrupa.kapacitet = int(kapacitet)
    izbornaGrupa.aktivna = aktivnost
    izbornaGrupa.save()

    return HttpResponse("<h1>Uspesno sacuvane izmene izborne grupe</h1>")


def izbor_grupe_form(request, username):
    student = Student.objects.get(nalog__username=username)
    izborneGrupe = IzbornaGrupa.objects.all()
    semestar = Semestar.objects.last()
    predmeti = Predmet.objects.all()

    context = {
        'student': student,
        'izborneGrupe': izborneGrupe,
        'semestar': semestar,
        'predmeti': predmeti,
    }
    return render(request, "studserviceapp/IzborGrupe.html", context)


def save_izbor_grupe(request):
    ostvarenoESPB = request.POST['broj_ostvarenih_espb']
    upisujeESPB = request.POST['student_upisuje_bodova']
    broj_polizenih_ispita = request.POST['broj_polozenih_ispit']
    upisuje_semestar = request.POST['vrsta_semestra']
    prvi_put_upisuje_semestar = request.POST['upis_semestra']
    nacin_placanja = request.POST['nacin_placanja']
    grupa_koju_student_bira = request.POST['grupe']
    username = request.POST['ime'][0].lower() + request.POST['prezime'].lower() + request.POST['godina_upisa'][-2:]
    student = Student.objects.get(nalog__username=username)

    if (IzborGrupe.objects.filter(student__broj_indeksa=student.broj_indeksa)):
        return HttpResponse("<h1> Student je vec izabrao grupu.</h1>")

    if (prvi_put_upisuje_semestar == "da"):
        prvi_put_upisuje_semestar = True
    else:
        if (prvi_put_upisuje_semestar == "ne"):
            prvi_put_upisuje_semestar = False

    if (request.POST['upisan'] == "da"):
        upisan = True
    else:
        if (request.POST['upisan'] == "ne"):
            upisan = False
    #
    # izbornaGrupa = IzbornaGrupa.objects.get(oznaka_semestra=grupa_koju_student_bira)
    # if(izbornaGrupa.kapacitet==0):
    #     return HttpResponse("<h1>Izborna grupa je popunjena, odaberite drugu grupu.</h1>")
    # else:
    #     izbornaGrupa.kapacitet -=1

    izborGrupe = IzborGrupe()

    izborGrupe.ostvarenoESPB = int(ostvarenoESPB)
    izborGrupe.upisujeESPB = int(upisujeESPB)
    izborGrupe.broj_polozenih_ispita = int(broj_polizenih_ispita)
    izborGrupe.upisuje_semestar = int(upisuje_semestar)

    izborGrupe.prvi_put_upisuje_semestar = prvi_put_upisuje_semestar
    izborGrupe.nacin_placanja = nacin_placanja
    izborGrupe.student = student
    izborGrupe.upisan = upisan

    # print(izborGrupe.ostvarenoESPB,
    #       izborGrupe.upisujeESPB,
    #       izborGrupe.broj_polozenih_ispita,
    #       izborGrupe.upisuje_semestar,
    #       izborGrupe.prvi_put_upisuje_semestar,
    #       izborGrupe.nacin_placanja,
    #       izborGrupe.student,
    #       izborGrupe.upisan)

    izborGrupe.save()

    nepolozeni_predmeti = request.POST.getlist('nepolozeniPredmeti')

    for p in nepolozeni_predmeti:
        predmet = Predmet.objects.get(naziv=p)
        izborGrupe.nepolozeni_predmeti.add(predmet)
    #     moze u html da se stavi value= {{p}} i odmah da se ubaci u predmete,
    #   ovako ima jedan vise pristup bazi
    return HttpResponse("<h1>Uspesno izvrsen izbor grupe</h1>")


def pregled_izabranih_grupa_form(request):
    grupe = IzbornaGrupa.objects.all()
    context = {
        'grupe': grupe
    }
    return render(request, 'studserviceapp/pregledIzabranihGrupa.html', context)


def pregled_studenata_u_izbornoj_grupi(request, grupa):
    student = Student.objects.all()
    studenti = student.filter(grupa__oznaka_grupe=grupa)
    context = {
        'studenti': studenti,
    }
    return render(request, "studserviceapp/pregledStudenataUIzbornojGrupi.html", context)


# class UploadRasporedaForm(forms.Form):
#     semestar = forms.ChoiceField(label='Raspored za semestar', choices=[(s.id, str(s)) for s in Semestar.objects.all()])
#     raspored_nastave = forms.FileField(label='Izaberite fajl')
#
#
# def upload_raspored_nastave(request, username):
#     if request.method == 'POST':
#         form = UploadRasporedaForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             sem = Semestar.objects.get(id=request.POST['semestar'])
#             # TODO
#             raspored_file = request.FILES['rasporedCSV']
#             # import_timetable_from_csv(raspored_file, sem)
#             return HttpResponse('Uspesno ste uneli raspored')
#     else:
#         form = UploadRasporedaForm()
#
#     return render(request, 'studserviceapp/upload_form.html', {'form': form})


def prikaz_obavestenja(request):
    obavestenja = Obavestenje.objects.all()
    return render(request, 'studserviceapp/prikaz_obavestenja.html', {'obavestenja': obavestenja})


def informacijeOStudentu(request, username):
    student = Student.objects.get(nalog__username=username)
    context = {
        'student': student,
    }
    return render(request, 'studserviceapp/InformacijeOStudentu.html', context)
