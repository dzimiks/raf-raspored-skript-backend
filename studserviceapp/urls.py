from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('timetable/<str:username>', views.timetableforuser, name='timetableforuser'),
    path('nastavnici.html', views.nastavnici_template, name = 'nastavnici'),
    path('unosobavestenja/<str:user>', views.unos_obavestenja_form, name = 'unosobavestenja'),
    path('unossemestra/<str:user>', views.unos_semestra_form, name = "unossemestra"),
    path('saveobavestenje',views.save_obavestenje, name = "saveobavestenje"),
    path('savesemestra', views.save_semestra, name = "savesemestra"),
    path('izmenaIzborneGrupe/<str:oznakaGrupe>',views.izmena_izborne_grupa_form,name="izmena_izborne_grupe"),
    path('saveIzmeneIzborneGrupe',views.save_izmene_izborne_grupe,name="save_izmene_izborne_grupe"),
    path('izborGrupe/<str:username>',views.izbor_grupe_form, name = "izbor_grupe"),
    path('saveIzborGrupe',views.save_izbor_grupe, name = 'save_izbor_grupe'),
    # url(r'^saveobavestenja/',views.save_obavestenje,name="saveobavestenje")
]
