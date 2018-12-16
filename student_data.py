import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from studserviceapp.models import Grupa, Nalog, Semestar, Student

mara = Nalog()
mara.username = 'marbutina'
mara.lozinka = 'lozinka'
mara.uloga = 'sekretar'
mara.save()

paxy = Nalog()
paxy.username = 'paxy'
paxy.lozinka = 'lozinka'
paxy.uloga = 'administrator'
paxy.save()

semestar = Semestar()
semestar.vrsta = "parni"
semestar.skolska_godina_pocetak = 2018
semestar.skolska_godina_kraj = 2019
semestar.save()

# Vanja
nalog_dzimiks = Nalog()
nalog_dzimiks.username = "vpaunovic16"
nalog_dzimiks.lozinka = "admir"
nalog_dzimiks.uloga = "student"
nalog_dzimiks.save()

grupa_dzimiks = Grupa.objects.get(oznaka_grupe="301")

dzimiks = Student()
dzimiks.ime = "Vanja"
dzimiks.prezime = "Paunovic"
dzimiks.broj_indeksa = 35
dzimiks.godina_upisa = 2016
dzimiks.smer = "RN"
dzimiks.nalog = nalog_dzimiks
dzimiks.save()
dzimiks.grupa.add(grupa_dzimiks)

# Milan
nalog_tkemi = Nalog()
nalog_tkemi.username = "mmitic16"
nalog_tkemi.lozinka = "admir"
nalog_tkemi.uloga = "student"
nalog_tkemi.save()

grupa_tkemi = Grupa.objects.get(oznaka_grupe="301")

tkemi = Student()
tkemi.ime = "Milan"
tkemi.prezime = "Mitic"
tkemi.broj_indeksa = 24
tkemi.godina_upisa = 2016
tkemi.smer = "RN"
tkemi.nalog = nalog_tkemi
tkemi.save()
tkemi.grupa.add(grupa_tkemi)

# Nemanja
nalog_nemanjan00 = Nalog()
nalog_nemanjan00.username = "nnedeljkovic15"
nalog_nemanjan00.lozinka = "admir"
nalog_nemanjan00.uloga = "student"
nalog_nemanjan00.save()

grupa_nemanjan00 = Grupa.objects.get(oznaka_grupe="302")

nemanjan00 = Student()
nemanjan00.ime = "Nemanja"
nemanjan00.prezime = "Nedeljkovic"
nemanjan00.broj_indeksa = 8
nemanjan00.godina_upisa = 2015
nemanjan00.smer = "RN"
nemanjan00.nalog = nalog_nemanjan00
nemanjan00.save()
nemanjan00.grupa.add(grupa_nemanjan00)
