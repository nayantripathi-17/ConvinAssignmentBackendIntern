from django.shortcuts import render
from django.http import JsonResponse,HttpResponseNotFound,HttpResponse
from django.shortcuts import redirect

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
import os

CLIENT_ID = os.getenv('CLIENT_ID')
PROJECT_ID = os.getenv('PROJECT_ID')
AUTH_URI = os.getenv('AUTH_URI')
TOKEN_URI = os.getenv('TOKEN_URI')
AUTH_PROVIDER_X509_CERT_URL = os.getenv('AUTH_PROVIDER_X509_CERT_URL')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URIS = str(os.getenv('REDIRECT_URIS')).split("&")
HOSTNAME = os.getenv('HOSTNAME')
SCOPES = str(os.getenv('SCOPES')).split("&")

flow = Flow.from_client_config({
   "web": {
       "client_id": CLIENT_ID,
       "project_id": PROJECT_ID,
       "auth_uri": AUTH_URI,
       "token_uri": TOKEN_URI,
       "auth_provider_x509_cert_url": AUTH_PROVIDER_X509_CERT_URL,
       "client_secret": CLIENT_SECRET,
       "redirect_uris": 
           REDIRECT_URIS,
       "javascript_origins": [
           HOSTNAME
       ]
   }
 },
 scopes=SCOPES,
 redirect_uri=REDIRECT_URIS[0])

def GoogleCalendarInitView(request):
  try:
    auth_url, _ = flow.authorization_url(prompt='consent',include_granted_scopes='true')
    return redirect(auth_url)
  except Exception as e: 
    print(e)
    return HttpResponseNotFound("Some error occured")

def GoogleCalendarRedirectView(request):
  try:
    code = request.GET.get("code")
    if(code==None):
      return HttpResponseNotFound("Code not sent")
  
    flow.fetch_token(code=code)
    credentials = flow.credentials
    service = build('calendar', 'v3', credentials=credentials,static_discovery=False)
    events = service.events().list(calendarId='primary',maxResults='2500').execute()
    return JsonResponse({"events":events})

  except Exception as e:
    print(e)
    return redirect("google_calendar:calendar_init")