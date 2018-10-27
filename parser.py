"""Parser za raspored časova, koji unosi podatke u bazu."""

import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet,Nalog,Semestar


# def clean_db():
    # Termin.objects.all().delete()
    # Predmet.objects.all().delete()
    # Nastavnik.objects.all().delete()
    # Grupa.objects.all().delete()
    # Nalog.objects.all().delete()


def import_timetable_from_csv(file_path):
    """Parser za raspored časova, koji unosi podatke u bazu."""
    state = -2
    header = []
    grupe = []
    predmet1 = None

    with open(file_path, encoding='utf-8') as csvfile:
        raspored_csv = csv.reader(csvfile, delimiter=';')

        for red in raspored_csv:

            if state == -2:
                state = -1

                # Naslov rasporeda

                continue

            if state == -1:
                state = 0

                grupe = red

                # Header za predavanje/praktikum/vezbe

                continue
            if not red:
                state = 0

                # Ako je linija prazna, ocekuje header u sledecoj liniji

                continue

            if state == 0:
                p = Predmet()
                p.naziv=red[0]
                p.save()
                predmet1=p

                # Novi predmet

                state = 1

                continue

            if state == 1:
                header = red

                # Header za predmete

                state = 2

                continue
            if state == 2:
                predmet = {}

                # Novi predmet i njegov praktikum/vezba/predavanje

                grupa = ""

                for key, column in enumerate(red):
                    if len(grupe) > key and grupe[key] != "":
                        grupa = grupe[key]

                    if column != "":
                        if grupa not in predmet:
                            predmet[grupa] = {}

                        predmet[grupa][header[key]] = column

                for key in predmet:
                    t = Termin()
                    t.predmet = predmet1

                    if(key == "Vezbe"):
                        t.tip_nastave = predmet[key]
                    if(key == "Predavanja"):
                        t.tip_nastave = predmet[key]
                    for k in predmet[key]:
                        if(k == "Uèionica"):
                            t.oznaka_ucionice =predmet[key][k]
                        if(k == "Dan"):
                            t.dan == predmet[key][k]
                        if(k == "Nastavnik(ci)"):
                            ime = predmet[key][k].split(" ")[1]
                            prezime = predmet[key][k].split(" ")[0]
                            username = (ime[0]).lower()+prezime.lower()
                            nal = Nalog()
                            nal.username = username
                            nal.lozinka = 'admin'
                            nal.save()
                            print(Nalog.objects.get(username = username1))

                            # nas = Nastavnik()
                            # nas.prezime = prezime
                            # nas.ime = ime
                            # print("ASDA")
                            # nas.nalog = Nalog.objects.get(username=nal.username)
                            # nas.save()

                        if(k == "Èas"):
                            t.pocetak = predmet[key][k].split("-")[0]
                            t.zavrsetak = predmet[key][k].split("-")[1]+":00"
                        if(k == "Odeljenje"):
                            gru = predmet[key][k].split(",")
                            gcount = len(gru)
                            for i in range(gcount):
                                g = Grupa()
                                g.oznaka_grupe = gru[i].strip()
                                # print(g.oznaka_grupe)
                                # g.save()
                            # grupe su dobro odvojene, ali ima neki problem

                    # t.save()

                    # ostao  je jos raspored koji ne znam kako da odradim

import_timetable_from_csv("./testData/rasporedCSV.csv")

