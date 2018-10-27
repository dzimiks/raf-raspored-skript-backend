"""Parser za raspored časova, koji unosi podatke u bazu."""

import csv
import os
import django
import datetime
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet, Nalog, Semestar

semestar = Semestar()
semestar.vrsta = "neparni"
semestar.skolska_godina_pocetak = 2018
semestar.skolska_godina_kraj = 2019
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
    predmet_object = None

    with open(file_path, encoding='utf-8') as csvfile:
        raspored_csv = csv.reader(csvfile, delimiter=';')

        for red in raspored_csv:
            # Naslov rasporeda
            if state == -2:
                state = -1
                continue

            # Header za predavanje/praktikum/vezbe
            if state == -1:
                state = 0
                grupe = red
                continue

            # Ako je linija prazna, ocekuje header u sledecoj liniji
            if not red:
                state = 0
                continue

            # Novi predmet
            if state == 0:
                predmet_object = Predmet()
                predmet_object.naziv = red[0]
                predmet_object.save()

                state = 1
                continue

            # Header za predmete
            if state == 1:
                header = red
                state = 2
                continue

            # Novi predmet i njegov praktikum/vezba/predavanje
            if state == 2:
                predmet = {}
                grupa = ""

                for key, column in enumerate(red):
                    if len(grupe) > key and grupe[key] != "":
                        grupa = grupe[key]

                    if column != "":
                        if grupa not in predmet:
                            predmet[grupa] = {}

                        predmet[grupa][header[key]] = column

                for key in predmet:
                    termin = Termin()
                    termin.predmet = predmet_object
                    termin.tip_nastave = key
                    termin.oznaka_ucionice = predmet[key]["Uèionica"]
                    termin.dan = predmet[key]["Dan"]
                    termin.pocetak = predmet[key]["Èas"].split("-")[0]
                    termin.zavrsetak = predmet[key]["Èas"].split("-")[1] + ":00"
                    termin.raspored = raspored

                    ime = predmet[key]["Nastavnik(ci)"].split(" ")[1]
                    prezime = predmet[key]["Nastavnik(ci)"].split(" ")[0]

                    # Bug sa mjovanovic
                    if ime == "Miljana" and prezime == "Jovanovic":
                        username = (ime[0]).lower() + "i" + prezime.lower()
                    else:
                        username = (ime[0]).lower() + prezime.lower()

                    # Bug sa Surlom jer je razmak u prezimenu
                    if ime == "Surla" and prezime == "Dimic":
                        username = "bdimicsurla"

                    # Bug sa Verom jer ima crticu u prezimenu
                    if prezime == "Vrbica-Matejic":
                        username = "vvrbicamatejic"

                    print(ime + " " + prezime + " -> " + username)

                    if Nalog.objects.filter(username=username).count() > 0:
                        nastavnik = Nastavnik.objects.get(ime=ime, prezime=prezime)
                    else:
                        nalog = Nalog()
                        nalog.username = username
                        nalog.lozinka = 'admin'
                        nalog.uloga = 'nastavnik'  # za sada su svi nastavnici
                        nalog.save()

                        nastavnik = Nastavnik()
                        nastavnik.ime = ime
                        nastavnik.prezime = prezime
                        nastavnik.titula = "dr"
                        nastavnik.zvanje = "mr"
                        nastavnik.nalog = nalog
                        nastavnik.save()
                        nastavnik.predmet.add(predmet_object)

                    termin.nastavnik = nastavnik
                    termin.save()

                    group_row = predmet[key]["Odeljenje"].split(",")

                    for i in group_row:
                        i = i.strip()

                        if Grupa.objects.filter(oznaka_grupe=i).count() > 0:
                            group = Grupa.objects.get(oznaka_grupe=i)
                        else:
                            group = Grupa()
                            group.oznaka_grupe = i
                            group.semestar = semestar
                            group.save()

                        termin.grupe.add(group)


import_timetable_from_csv("./testData/rasporedCSV.csv")
