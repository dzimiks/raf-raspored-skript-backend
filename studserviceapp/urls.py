from django.urls import path
from . import views
from django.conf.urls import url
from django.shortcuts import redirect


def redirect_view(request):
    response = redirect('/redirect-success/')
    return response


urlpatterns = [
    path('timetable/<str:username>', views.timetableforuser, name='timetableforuser'),
    path('nastavnici.html', views.nastavnici_template, name='nastavnici'),
    path('unosobavestenja/<str:user>', views.unos_obavestenja_form, name='unosobavestenja'),
    path('saveobavestenje', views.save_obavestenje, name="saveobavestenje"),
    path('unossemestra/<str:user>', views.unos_semestra_form, name="unossemestra"),
    path('savesemestra', views.save_semestra, name="savesemestra"),
    path('izmenaIzborneGrupe/<str:oznakaGrupe>/<str:vrstaSemestra>', views.izmena_izborne_grupa_form,
         name="izmena_izborne_grupe"),
    path('saveIzmeneIzborneGrupe', views.save_izmene_izborne_grupe, name="save_izmene_izborne_grupe"),
    path('izborGrupe/<str:username>', views.izbor_grupe_form, name="izbor_grupe"),
    path('saveIzborGrupe', views.save_izbor_grupe, name='save_izbor_grupe'),
    path('pregledIzabranihGrupa', views.pregled_izabranih_grupa_form, name="pregled_izabranih_grupa"),
    path('pregledStudenataIzborneGrupa/<str:grupa>', views.pregled_studenata_u_izbornoj_grupi,
         name="pregled_studenata_u_izbornim_grupama"),
    path('informacijeOstudentu/<str:username>', views.informacijeOStudentu, name="informacije_o_studentu"),
    url(r'^saveobavestenja/', views.save_obavestenje, name="saveobavestenje"),
    path('prikaz_obavestenja', views.prikaz_obavestenja, name="prikaz_obavestenja"),
    path('upload_form/<str:username>', views.upload_raspored_nastave, name='upload_form'),
    path('professor_grupe/<str:username>', views.professor_grupe, name='professor_grupe'),
    path('spisak_po_grupi/<str:oznaka_grupe>', views.spisak_po_grupi, name='spisak_po_grupi')
]
