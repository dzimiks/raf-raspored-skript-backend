from django.urls import path
from . import views


urlpatterns = [
    path('timetable/<str:username>', views.timetableforuser, name='timetableforuser'),
    path('nastavnici.html', views.nastavnici_template, name = 'nastavnici'),
    path('unosobavestenja/<str:user>', views.unos_obavestenja_form, name = 'unosobavestenja'),
]
