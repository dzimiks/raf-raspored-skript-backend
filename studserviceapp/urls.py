from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('timetable/<str:username>', views.timetableforuser, name='timetableforuser'),
    path('nastavnici.html', views.nastavnici_template, name = 'nastavnici'),
    path('unosobavestenja/<str:user>', views.unos_obavestenja_form, name = 'unosobavestenja'),
    path('unossemestra/<str:user>', views.unos_semestra_form, name = "unossemestra"),
    url(r'^savesemestra/',views.save_semestra,name="savesemestra"),
    url(r'^saveobavestenja/',views.save_obavestenje,name="saveobavestenje")
]
