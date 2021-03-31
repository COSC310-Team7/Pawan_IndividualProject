import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

APIToken = 'token.pickle'
APICredential = 'credentials.json'


def authenticated_service(scopes=['https://www.googleapis.com/auth/calendar',
                                  'https://www.googleapis.com/auth/calendar.events'
                                  ]):
    credentials = None

    if os.path.exists(APIToken):
        with open(APIToken, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(APICredential, scopes)
            credentials = flow.run_local_server(port=0)
        with open(APIToken, 'wb') as token:
            pickle.dump(credentials, token)

    service = build('calendar', 'v3', credentials=credentials)
    return service


def event_list(calendar='primary', min_datetime=datetime.datetime.utcnow(), upcoming_events=10):
    service = authenticated_service()

    min_time = min_datetime.isoformat() + 'Z'

    events_result = service.events().list(calendarId=calendar,
                                          timeMin=min_time,
                                          maxResults=upcoming_events,
                                          singleEvents=True,
                                          orderBy='startTime'
                                          ).execute()
    events = events_result.get('items', [])
    return events


def calendar_list():
    service = authenticated_service()
    page_token = None
    next_token = True
    calendars = []
    while next_token:
        calendar_result = service.calendarList().list(pageToken=page_token).execute()
        for entry in calendar_result['items']:
            calendars.append(entry)
        page_token = calendar_result.get('nextPageToken')
        if not page_token:
            next_token = False
    return calendars


def insert_event(event, calendarId='primary'):
    service = authenticated_service()
    service.events().insert(calendarId=calendarId, body=event, sendNotifications=True).execute()


def get_event(eventId, calendarId='primary'):
    service = authenticated_service()
    return service.events().get(calendarId=calendarId, eventId=eventId).execute()


def remove_event(eventId, calendarId='primary'):
    service = authenticated_service()
    return service.events().delete(calendarId=calendarId, eventId=eventId).execute()


def event_instances(eventId, calendarId='primary'):
    service = authenticated_service()
    page_token = None
    next_token = True
    events = []
    while next_token:
        events_result = service.events().instances(calendarId=calendarId, eventId=eventId, pageToken=page_token).execute()
        for entry in events_result:
            events.append(entry)
        page_token = events_result.get('nextPageToken')
        if not page_token:
            next_token = False
    return events

