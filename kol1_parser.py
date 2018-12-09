import json
import csv
import os
import django
import datetime

from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from studserviceapp.models import RasporedPolaganja, TerminPolaganja, Predmet, Nastavnik


def parse(file_path):
    with open(file_path, encoding='utf-8') as file:
        k1_csv = csv.reader(file, delimiter=',')
        header = next(k1_csv)
        header = list(filter(None, header))
        # header = list(filter(lambda a: a != '', header))

        lessons = list()
        professors = list()
        classrooms = list()
        times = list()
        days = list()
        dates = list()
        kol1 = dict()
        all = list()

        for row in k1_csv:
            row = list(filter(None, row))
            nastavnik = Nastavnik()
            predmet = Predmet()
            raspored_polaganja = RasporedPolaganja()
            termin_polaganja = TerminPolaganja()
            element = dict()

            lesson = row[0]
            professor = row[1]
            classroom = row[2]
            time = row[3]
            day = row[4]
            date = row[5]

            print(professor)

            lessons.append(lesson)
            professors.append(professor)
            classrooms.append(classroom)
            times.append(time)
            days.append(day)
            dates.append(date)

            element[header[0]] = lesson
            element[header[1]] = professor
            element[header[2]] = classroom
            element[header[3]] = time
            element[header[4]] = day
            element[header[5]] = date

            all.append(element)

        kol1['kol1'] = all
        print(json.dumps(kol1, indent=4))


parse('./testData/kol1.csv')