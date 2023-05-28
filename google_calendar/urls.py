from django.urls import path
from django.conf.urls import url
from . import views

app_name='google_calendar'

urlpatterns = [
  url(r'^init',views.GoogleCalendarInitView, name="calendar_init"),
  url(r'^redirect',views.GoogleCalendarRedirectView, name="calendar_redirect")
]