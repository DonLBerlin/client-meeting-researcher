#!/usr/bin/env python3
"""
Fetch upcoming Google Calendar events with external attendees.

Prerequisites:
  pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

Setup:
  1. Go to https://console.cloud.google.com/
  2. Create a project, enable Google Calendar API
  3. Create OAuth 2.0 credentials (Desktop App), download as credentials.json
  4. Place credentials.json in ~/.claude/skills/client-meeting-researcher/
  5. Run this script once to authorize — token.json will be saved for future use

Usage:
  python3 fetch_calendar.py [--days 7] [--my-domain yourcompany.com]
"""

import json
import sys
import os
import argparse
from datetime import datetime, timedelta, timezone

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CREDENTIALS_PATH = os.path.expanduser("~/.claude/skills/client-meeting-researcher/credentials.json")
TOKEN_PATH = os.path.expanduser("~/.claude/skills/client-meeting-researcher/token.json")


def get_service():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                print(json.dumps({
                    "error": f"credentials.json not found at {CREDENTIALS_PATH}. "
                             "Download OAuth2 credentials from Google Cloud Console and place them there."
                }))
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def is_external(email: str, my_domain: str) -> bool:
    if not email:
        return False
    domain = email.lower().split("@")[-1]
    return domain != my_domain.lower() and not domain.endswith(".google.com")


def fetch_upcoming_external_meetings(days: int, my_domain: str):
    service = get_service()
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime",
        maxResults=50,
    ).execute()

    events = events_result.get("items", [])
    output = []

    for event in events:
        attendees = event.get("attendees", [])
        if not attendees:
            continue

        external = [
            {
                "email": a.get("email", ""),
                "name": a.get("displayName", ""),
                "responseStatus": a.get("responseStatus", ""),
            }
            for a in attendees
            if is_external(a.get("email", ""), my_domain)
            and not a.get("resource", False)
        ]

        if not external:
            continue

        start = event.get("start", {})
        output.append({
            "summary": event.get("summary", "(No title)"),
            "start": start.get("dateTime", start.get("date", "")),
            "end": event.get("end", {}).get("dateTime", ""),
            "location": event.get("location", ""),
            "description": event.get("description", ""),
            "meetLink": event.get("hangoutLink", ""),
            "externalAttendees": external,
        })

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Google Calendar external meetings")
    parser.add_argument("--days", type=int, default=7, help="Look-ahead window in days (default: 7)")
    parser.add_argument("--my-domain", required=True, help="Your company email domain (e.g. acme.com)")
    args = parser.parse_args()

    fetch_upcoming_external_meetings(args.days, args.my_domain)
