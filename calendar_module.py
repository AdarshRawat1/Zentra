import datetime
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from vision_module import VisionModule
from gemini_module import GeminiModule
import pyautogui
import json

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

class CalendarModule:
    def __init__(self):
        self.creds = None
        if os.path.exists(TOKEN_FILE):
            self.creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('calendar', 'v3', credentials=self.creds)

    def list_events(self, max_results=10):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                  maxResults=max_results, singleEvents=True,
                                                  orderBy='startTime').execute()
        return events_result.get('items', [])

    def create_event(self, summary, start_time, end_time):
        event = {
            'summary': summary,
            'start': {'dateTime': start_time, 'timeZone': 'UTC'},
            'end': {'dateTime': end_time, 'timeZone': 'UTC'},
        }
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        return event

    def delete_event(self, event_id):
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()
        return True

    def sync_with_google(self):
        print("Syncing with Google Calendar...")
        events = self.list_events()
        print(f"Upcoming events: {len(events)}")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
        return events

    def handle_gemini_intent(self, user_command):
        gemini = GeminiModule()
        intent = gemini.interpret_command(f"Interpret this as a Google Calendar command: {user_command}. Respond with JSON: {{'action': 'list'|'create'|'delete', 'summary': str, 'start_time': str, 'end_time': str, 'event_id': str}}.")
        try:
            parsed = json.loads(intent)
        except Exception as e:
            print(f"Could not parse Gemini intent: {e}")
            return None
        action = parsed.get('action')
        if action == 'list':
            return self.list_events()
        elif action == 'create':
            return self.create_event(parsed['summary'], parsed['start_time'], parsed['end_time'])
        elif action == 'delete':
            return self.delete_event(parsed['event_id'])
        else:
            print("Unknown action.")
            return None

vision = VisionModule()
gemini = GeminiModule()

# Step 1: Open WhatsApp (already done)
# Step 2: Take screenshot and analyze
screenshot = vision.capture_screenshot()
description = gemini.vision_analyze(
    "Describe what is currently visible on WhatsApp Web. Is the chat list visible? Is there a search box? Are there any popups?",
    screenshot
)
print(description)
# Step 3: Decide next action based on description
# (e.g., if chat list is visible, proceed; if not, ask user or retry)

while not task_complete:
    screenshot = vision.capture_screenshot()
    description = gemini.vision_analyze("What is on the screen? What should I do next?", screenshot)
    action = decide_next_action(description)
    perform_action(action) 