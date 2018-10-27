from django.urls import path
from . import views

urlpatterns = [
    path('timetable/<str:username>', views.timetableforuser, name='timetableforuser'),
]
