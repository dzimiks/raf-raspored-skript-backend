import json
import csv
import os
import django
import codecs
import datetime
from datetime import datetime

from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from studserviceapp.models import RasporedPolaganja, TerminPolaganja, Predmet, Nastavnik, Nalog


def parse(file, semestar, kolokvijumska_nedelja):
    k1_csv = csv.reader(codecs.iterdecode(file, 'utf-8'), delimiter=',')
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

    svi_predmeti = Predmet.objects.all()
    svi_nastavnici = Nastavnik.objects.all()
    line_count = 2

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

        lessons.append(lesson)
        professors.append(professor)
        classrooms.append(classroom)
        times.append(time)
        days.append(day)
        dates.append(date)

        print('Lesson:', lesson)
        print('Professor:', professor)
        print('Classroom:', classroom)
        print('Time:', time)
        print('Day:', day)
        print('Date:', date)
        print('Ime:', professor.split(',')[0].split(' ')[0])

        prof = professor.split(',')
        profy = professor.lstrip().split(' ')

        # print('PROF:', prof)
        # print('PROF LEN:', len(prof))
        # print('Profy:', profy)
        # print('Profy LEN:', len(profy))

        # TODO dan
        if day not in ('Ponedeljak', 'Utorak', 'Sreda', 'Četvrtak', 'Petak', 'Subota', 'Nedelja'):
            print('>>> ERROR ON LINE ' + str(line_count) + ': Nepoznat dan -> ' + day)

        # TODO predmet
        if lesson not in (p.naziv for p in svi_predmeti):
            print('>>> ERROR ON LINE ' + str(line_count) + ': Nepoznat predmet -> ' + lesson)
            predmet.naziv = lesson
            predmet.save()
            termin_polaganja.predmet = predmet
        else:
            predmet = Predmet.objects.get(naziv=lesson)
            # predmet.save()
            print('@@@@@@@@@', predmet)
            # predmet.naziv = lesson
            # nastavnik.predmet = predmet
            termin_polaganja.predmet = predmet

        # TODO ucionica
        class_flag = True

        for c in classroom.split(','):
            if c not in (
                '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                'RG1', 'RG2', 'RG3', 'RG4', 'RG5', 'RG6', 'RG7', 'Atelje'):
                print('>>> ERROR ON LINE ' + str(line_count) + ': Nepoznata ucionica -> ' + c)
                class_flag = False

        if class_flag:
            termin_polaganja.ucionice = classroom

        # TODO DATES
        date_flag = True

        # TODO vreme
        if len(time.split('-')) != 2:
            print('>>> ERROR ON LINE ' + str(line_count) + ': Nepoznata vreme -> ' + time)
            date_flag = False

        # TODO datum
        if len(date.split('.')) != 3:
            print('>>> ERROR ON LINE ' + str(line_count) + ': Nepoznat datum -> ' + date)
            date_flag = False

        if date_flag:
            # TODO Parsing dates
            string_date = date + str(datetime.now().year)
            print('STRING DATE:', string_date)

            final_date = datetime.strptime(string_date, '%d.%m.%Y')
            print('FINAL DATE:', final_date)

            string_start = string_date + ' ' + time.split('-')[0]
            print('STRING START:', string_start)
            final_start = datetime.strptime(string_start, '%d.%m.%Y %H')
            print('FINAL START:', final_start)

            string_end = string_date + ' ' + time.split('-')[1]
            print('STRING END:', string_end)
            final_end = datetime.strptime(string_end, '%d.%m.%Y %H')
            print('FINAL END:', final_end)

            termin_polaganja.pocetak = final_start
            termin_polaganja.zavrsetak = final_end
            termin_polaganja.datum = final_date

        # TODO nastavnik
        if (len(prof) == 1) and (len(profy) == 2):
            nastavnik.ime = prof[0].lstrip().split(' ')[0]
            nastavnik.prezime = prof[0].lstrip().split(' ')[1]

            print('>>> NASTAVNIK IME:', nastavnik.ime)
            print('>>> NASTAVNIK PREZIME:', nastavnik.prezime)

            if not (nastavnik.ime, nastavnik.prezime) in ((n.ime, n.prezime) for n in svi_nastavnici):
                print('>>> ERROR ON LINE ' + str(line_count) + ':', nastavnik.ime, nastavnik.prezime,
                      'ne postoji u bazi!')
                nalog = Nalog()
                nalog.username = (nastavnik.ime[0]).lower() + nastavnik.prezime.lower()
                nalog.save()
                nastavnik.nalog = nalog
                nastavnik.save()
                termin_polaganja.nastavnik = nastavnik
            else:
                # TODO
                nalog = Nalog()
                nalog.username = (nastavnik.ime[0]).lower() + nastavnik.prezime.lower()
                nalog.save()
                nastavnik = Nastavnik.objects.get(nalog__username=nalog.username)
                # nastavnik.save()
                termin_polaganja.nastavnik = nastavnik
        else:
            for p in prof:
                nastavnik.ime = p.lstrip().split(' ')[0]
                nastavnik.prezime = p.lstrip().split(' ')[1]

                print('>>> NASTAVNIK IME:', nastavnik.ime)
                print('>>> NASTAVNIK PREZIME:', nastavnik.prezime)

                if not (nastavnik.ime, nastavnik.prezime) in ((n.ime, n.prezime) for n in svi_nastavnici):
                    print('>>> ERROR ON LINE ' + str(line_count) + ':', nastavnik.ime, nastavnik.prezime,
                          'ne postoji u bazi!')
                    nalog = Nalog()
                    nalog.username = (nastavnik.ime[0]).lower() + nastavnik.prezime.lower()
                    nalog.save()
                    nastavnik.nalog = nalog
                    nastavnik.save()
                    termin_polaganja.nastavnik = nastavnik
                else:
                    # TODO
                    nalog = Nalog()
                    nalog.username = (nastavnik.ime[0]).lower() + nastavnik.prezime.lower()
                    nalog.save()
                    nastavnik = Nastavnik.objects.get(nalog__username=nalog.username)
                    # nastavnik.save()
                    termin_polaganja.nastavnik = nastavnik
        print()

        # TODO
        raspored_polaganja.kolokvijumska_nedelja = kolokvijumska_nedelja
        raspored_polaganja.save()

        # TODO
        termin_polaganja.raspored_polaganja = raspored_polaganja
        termin_polaganja.save()

        element[header[0]] = lesson
        element[header[1]] = professor
        element[header[2]] = classroom
        element[header[3]] = time
        element[header[4]] = day
        element[header[5]] = date

        all.append(element)

        line_count += 1

    kol1['kol1'] = all
    # print(json.dumps(kol1, indent=4))
