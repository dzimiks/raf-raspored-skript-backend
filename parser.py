"""Parser za raspored časova, koji unosi podatke u bazu."""

import csv
import os
import django
import datetime
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet, Nalog, Semestar

# def clean_db():
# Termin.objects.all().delete()
# Predmet.objects.all().delete()
# Nastavnik.objects.all().delete()
# Grupa.objects.all().delete()
# Nalog.objects.all().delete()

# timezone.now()

semestar = Semestar()
semestar.vrsta = "parni"
semestar.skolska_godina_kraj = 2019
semestar.skolska_godina_pocetak = 2018
semestar.save()

raspored = RasporedNastave()
raspored.datum_unosa = datetime.datetime.now(tz=timezone.utc)
raspored.semestar = semestar
raspored.save()


def import_timetable_from_csv(file_path):
    """Parser za raspored časova, koji unosi podatke u bazu."""
    state = -2
    header = []
    grupe = []
    predmetObject = None

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
                predmetObject = Predmet()
                predmetObject.naziv = red[0]
                predmetObject.save()

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
                    t.predmet = predmetObject
                    t.tip_nastave = key
                    t.oznaka_ucionice = predmet[key]["Uèionica"]
                    t.dan = predmet[key]["Dan"]
                    t.pocetak = predmet[key]["Èas"].split("-")[0]
                    t.zavrsetak = predmet[key]["Èas"].split("-")[1] + ":00"

                    ime = predmet[key]["Nastavnik(ci)"].split(" ")[1]
                    prezime = predmet[key]["Nastavnik(ci)"].split(" ")[0]

                    # Bug sa mjovanovic
                    if ime == "Miljana" and prezime == "Jovanovic":
                        username = (ime[0]).lower() + "i" + prezime.lower()
                    else:
                        username = (ime[0]).lower() + prezime.lower()

                    print(ime + " " + prezime + " " + username)
                    # nastavnik = None

                    if Nalog.objects.filter(username=username).count() > 0:
                        nastavnik = Nastavnik.objects.get(ime=ime, prezime=prezime)
                    else:
                        nal = Nalog()
                        nal.username = username
                        nal.lozinka = 'admin'
                        nal.save()

                        nastavnik = Nastavnik()
                        nastavnik.ime = ime
                        nastavnik.prezime = prezime
                        nastavnik.titula = "dr"
                        nastavnik.zvanje = "mr"
                        nastavnik.nalog = nal

                        nastavnik.save()
                        nastavnik.predmet.add(predmetObject)

                    t.nastavnik = nastavnik
                    t.raspored = raspored

                    t.save()

                    gru = predmet[key]["Odeljenje"].split(",")

                    for i in gru:
                        i = i.strip()

                        if Grupa.objects.filter(oznaka_grupe=i).count() > 0:
                            g = Grupa.objects.get(oznaka_grupe=i)
                        else:
                            g = Grupa()
                            g.oznaka_grupe = i
                            g.semestar = semestar
                            g.save()

                        t.grupe.add(g)

                # ostao  je jos raspored koji ne znam kako da odradim


import_timetable_from_csv("./testData/rasporedCSV.csv")
