"""Parser za raspored časova, koji unosi podatke u bazu."""

import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from studserviceapp.models import Grupa, Nastavnik, Termin, RasporedNastave, Predmet


def import_timetable_from_csv(file_path):
    """Parser za raspored časova, koji unosi podatke u bazu."""
    state = -2
    header = []
    naziv_predmeta = ""
    grupe = []

    with open(file_path, encoding='utf-8') as csvfile:
        raspored_csv = csv.reader(csvfile, delimiter=';')
        for red in raspored_csv:
            if state == -2:
                state = -1

                continue

            if state == -1:
                state = 0

                grupe = red

                continue
            if not red:
                state = 0

                continue

            if state == 0:
                naziv_predmeta = red[0]

                state = 1

                continue

            if state == 1:
                header = red

                state = 2

                continue
            if state == 2:
                predmet = {}

                predmet["naziv"] = naziv_predmeta

                grupa = ""

                for key, column in enumerate(red):
                    if len(grupe) > key and grupe[key] != "":
                        grupa = grupe[key]

                    if column != "":
                        if grupa not in predmet:
                            predmet[grupa] = {}

                        predmet[grupa][header[key]] = column

                print(predmet)


import_timetable_from_csv("./testData/rasporedCSV.csv")
