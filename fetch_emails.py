import os
import pickle
import base64
import re
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from database import store_meeting

# Google API Setup
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate with Gmail API."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def get_email_body(message):
    """Extract the body from the email."""
    try:
        payload = message['payload']
        parts = payload.get('parts', [])
        
        for part in parts:
            if part['mimeType'] == 'text/plain':
                return part['body']['data']
        if 'body' in payload:
            return payload['body']['data']
    except KeyError:
        return None

def parse_meeting_details(email_body):
    """Parse meeting details like date, time, participants, and location from email body."""
    date_time_pattern = r"(?:on|at)?\s*(\b(?:[0-9]{1,2}[\/\-]?[0-9]{1,2}[\/\-]?[0-9]{2,4})\b.*?(?:at|pm|am)?)"
    date_time_match = re.search(date_time_pattern, email_body, re.IGNORECASE)
    
    participants_pattern = r"([a-zA-Z]+[ ]*[a-zA-Z]+[ ]*<[^>]+>)"
    participants_match = re.findall(participants_pattern, email_body)
    
    location_pattern = r"(?:location|place|venue).*?([a-zA-Z0-9\s,]+)"
    location_match = re.search(location_pattern, email_body, re.IGNORECASE)

    meeting_details = {
        'datetime': date_time_match.group(1) if date_time_match else None,
        'participants': participants_match,
        'location': location_match.group(1) if location_match else None,
    }

    return meeting_details

def get_emails():
    service = authenticate_gmail()

    try:
        # Fetch emails with meeting-related content
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="meeting OR invite OR appointment").execute()
        messages = results.get('messages', [])

        if not messages:
            print('No new messages.')
        else:
            print('Messages:')
            for message in messages[:5]:  # Limit to first 5 messages for now
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                email_body = get_email_body(msg)

                if email_body:
                    # Decode the base64url encoded email body
                    decoded_body = email_body.replace('-', '+').replace('_', '/')
                    decoded_body = base64.urlsafe_b64decode(decoded_body).decode('utf-8')

                    print("Email Body: ", decoded_body)
                    meeting_details = parse_meeting_details(decoded_body)

                    # Store meeting details in the database
                    store_meeting(meeting_details['datetime'], ', '.join(meeting_details['participants']), meeting_details['location'])
                    print("Meeting Details Stored:", meeting_details)
                print('-' * 50)

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    get_emails()
