import json
import csv
import os
import django
import codecs
import datetime

from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from studserviceapp.models import RasporedPolaganja, TerminPolaganja, Predmet, Nastavnik


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

        print('PROF:', prof)
        print('PROF LEN:', len(prof))
        print('Profy:', profy)
        print('Profy LEN:', len(profy))

        if (len(prof) == 1) and (len(profy) == 2):
            nastavnik.ime = prof[0].lstrip().split(' ')[0]
            nastavnik.prezime = prof[0].lstrip().split(' ')[1]

            print('>>> NASTAVNIK IME:', nastavnik.ime)
            print('>>> NASTAVNIK PREZIME:', nastavnik.prezime)

            if not (nastavnik.ime, nastavnik.prezime) in ((n.ime, n.prezime) for n in svi_nastavnici):
                print('>>> ERROR ON LINE ' + str(line_count) + ':', nastavnik.ime, nastavnik.prezime,
                      'ne postoji u bazi!')
            else:
                # TODO
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
                else:
                    # TODO
                    termin_polaganja.nastavnik = nastavnik

        # TODO
        if day not in ('Ponedeljak', 'Utorak', 'Sreda', 'Četvrtak', 'Petak', 'Subota', 'Nedelja'):
            print('>>> ERROR ON LINE ' + str(line_count) + ': Nepoznat dan -> ' + day)

        # TODO
        if lesson not in (p.naziv for p in svi_predmeti):
            print('>>> ERROR ON LINE ' + str(line_count) + ': Nepoznat predmet -> ' + lesson)

        # TODO
        for c in classroom.split(','):
            if c not in (
                '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                'RG1', 'RG2', 'RG3', 'RG4', 'RG5', 'RG6', 'RG7', 'Atelje'):
                print('>>> ERROR ON LINE ' + str(line_count) + ': Nepoznata ucionica -> ' + c)

        # TODO
        if len(time.split('-')) != 2:
            print('>>> ERROR ON LINE ' + str(line_count) + ': Nepoznata vreme -> ' + time)

        # TODO
        if len(date.split('.')) != 3:
            print('>>> ERROR ON LINE ' + str(line_count) + ': Nepoznat datum -> ' + date)

        print('Pre:', time.split('-')[0])
        print('Posle:', time.split('-')[1])
        print()

        raspored_polaganja.kolokvijumska_nedelja = kolokvijumska_nedelja

        predmet.naziv = lesson

        # nastavnik.ime = professor.split(',')[0].split(' ')[0]
        # nastavnik.prezime = professor.split(',')[0].split(' ')[1:]

        termin_polaganja.ucionice = classroom
        termin_polaganja.pocetak = time.split('-')[0]
        termin_polaganja.zavrsetak = time.split('-')[1]
        termin_polaganja.datum = date
        termin_polaganja.raspored_polaganja = raspored_polaganja
        termin_polaganja.predmet = predmet

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
