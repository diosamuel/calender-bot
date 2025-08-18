"""
Google Calendar Service
Handles all Google Calendar API operations
"""
import os
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config

class GoogleCalendarService:
    def __init__(self):
        self.service = None
        self.credentials = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate and create Google Calendar service"""
        creds = None
        
        # Token file stores the user's access and refresh tokens
        if os.path.exists(config.GOOGLE_TOKEN_FILE):
            with open(config.GOOGLE_TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(config.GOOGLE_CREDENTIALS_FILE):
                    raise FileNotFoundError(
                        f"Credentials file '{config.GOOGLE_CREDENTIALS_FILE}' not found. "
                        "Please download it from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.GOOGLE_CREDENTIALS_FILE, 
                    config.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(config.GOOGLE_TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        
        self.credentials = creds
        self.service = build('calendar', 'v3', credentials=creds)
    
    def create_event(self, 
                    summary: str, 
                    start_time: datetime, 
                    end_time: datetime,
                    description: str = None,
                    location: str = None,
                    attendees: List[str] = None) -> Dict:
        """
        Create a new calendar event
        """
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': config.TIMEZONE_STR,
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': config.TIMEZONE_STR,
            },
        }
        
        if description:
            event['description'] = description
        
        if location:
            event['location'] = location
        
        if attendees:
            event['attendees'] = [{'email': email} for email in attendees]
        
        try:
            event = self.service.events().insert(
                calendarId='primary', 
                body=event
            ).execute()
            return event
        except HttpError as error:
            raise Exception(f'An error occurred: {error}')
    
    def list_events(self, 
                   time_min: datetime = None, 
                   time_max: datetime = None,
                   max_results: int = 10) -> List[Dict]:
        """
        List calendar events within a time range
        """
        if not time_min:
            time_min = datetime.now(config.TIMEZONE)
        
        if not time_max:
            time_max = time_min + timedelta(days=1)
        
        try:
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=time_min.isoformat(),
                timeMax=time_max.isoformat(),
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return events
        except HttpError as error:
            raise Exception(f'An error occurred: {error}')
    
    def get_todays_events(self) -> List[Dict]:
        """Get all events for today"""
        now = datetime.now(config.TIMEZONE)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        return self.list_events(start_of_day, end_of_day)
    
    def get_week_events(self) -> List[Dict]:
        """Get all events for this week"""
        now = datetime.now(config.TIMEZONE)
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + timedelta(days=7)
        
        return self.list_events(start_of_week, end_of_week, max_results=50)
    
    def update_event(self, 
                    event_id: str,
                    summary: str = None,
                    start_time: datetime = None,
                    end_time: datetime = None,
                    description: str = None,
                    location: str = None) -> Dict:
        """
        Update an existing calendar event
        """
        try:
            # First, get the existing event
            event = self.service.events().get(
                calendarId='primary', 
                eventId=event_id
            ).execute()
            
            # Update fields if provided
            if summary:
                event['summary'] = summary
            
            if start_time:
                event['start'] = {
                    'dateTime': start_time.isoformat(),
                    'timeZone': config.TIMEZONE_STR,
                }
            
            if end_time:
                event['end'] = {
                    'dateTime': end_time.isoformat(),
                    'timeZone': config.TIMEZONE_STR,
                }
            
            if description is not None:
                event['description'] = description
            
            if location is not None:
                event['location'] = location
            
            # Update the event
            updated_event = self.service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event
            ).execute()
            
            return updated_event
        except HttpError as error:
            raise Exception(f'An error occurred: {error}')
    
    def delete_event(self, event_id: str) -> bool:
        """
        Delete a calendar event
        """
        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=event_id
            ).execute()
            return True
        except HttpError as error:
            raise Exception(f'An error occurred: {error}')
    
    def search_events(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search for events by text query
        """
        try:
            now = datetime.now(config.TIMEZONE)
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now.isoformat(),
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime',
                q=query
            ).execute()
            
            events = events_result.get('items', [])
            return events
        except HttpError as error:
            raise Exception(f'An error occurred: {error}')