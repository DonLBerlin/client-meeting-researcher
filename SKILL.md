---
name: client-meeting-researcher
description: Researches external clients from upcoming Google Calendar meetings and generates pre-meeting briefing reports. This skill should be used when the user wants to prepare for a client meeting, research who they're meeting with, get a summary of an external contact, or get conversation starters for an upcoming meeting.
---

# Client Meeting Researcher

Fetch upcoming Google Calendar meetings, identify external attendees, research them online, and produce a pre-meeting briefing with professional background, online presence, and conversation starters.

## Prerequisites

Install the Google Calendar API client library:

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### First-time Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select existing), then enable **Google Calendar API**
3. Go to **APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID** (Desktop App)
4. Download the JSON file and save it as:
   `~/.claude/skills/client-meeting-researcher/credentials.json`
5. Run the fetch script once — a browser window will open for authorization, and `token.json` is saved automatically for future runs

## Workflow

### Step 1: Ask for User's Company Domain

Ask the user for their company email domain (e.g., `acme.com`) if not already known — this distinguishes internal from external attendees. Also confirm the look-ahead window (default: 7 days).

### Step 2: Fetch External Meetings from Google Calendar

Run the fetch script:

```bash
python3 ~/.claude/skills/client-meeting-researcher/scripts/fetch_calendar.py \
  --my-domain <THEIR_DOMAIN> \
  --days <DAYS>
```

The script outputs a JSON array of meetings with at least one external attendee. Each item includes:
- `summary` — meeting title
- `start` / `end` — ISO timestamps
- `externalAttendees` — list of `{email, name, responseStatus}`
- `location`, `description`, `meetLink`

If the output is `[]`, inform the user there are no upcoming external meetings in that window.

If the script errors with a credentials message, walk the user through the OAuth setup above.

### Step 3: Present Meeting List and Confirm Scope

Show upcoming external meetings in a clean numbered list with date/time and attendee names. Ask which meeting(s) to research. If there is only one, proceed automatically.

### Step 4: Research Each External Attendee

For each external attendee, run multiple targeted web searches:

**Professional background:**
- `"[full name]" "[company from email domain]" title OR role`
- `"[full name]" site:linkedin.com/in`

**Online presence:**
- LinkedIn: follower count, recent posts/activity themes
- Twitter/X: `"[full name]" site:twitter.com OR site:x.com`
- Blog, podcast appearances, conference talks, publications

**Recent news:**
- `"[full name]" "[company]" 2025 news`
- Company announcements, product launches, funding rounds

**Interests and personality signals:**
- Topics they post about, causes they support, hobbies mentioned publicly

When the name is common, add the company name extracted from the email domain to narrow results. If online presence is sparse, focus on the company's news and industry context instead.

### Step 5: Generate Pre-Meeting Briefing

Produce a structured briefing for each selected meeting. Use this format:

---

## Pre-Meeting Briefing: [Meeting Title]
**Date:** [Date & Time] | **Duration:** [X min if determinable]

---

### [Attendee Full Name]
**Title:** [Current title] at [Company]
**Email:** [email]

#### Professional Background
[2–3 sentences: career arc, current role scope, notable achievements or past companies]

#### Online Presence
- **LinkedIn:** [URL if found] — [follower count if available]
  - Recent focus: [topics/themes from posts or activity]
- **Twitter/X:** [@handle] — [follower count]
  - Engages with: [topics/themes]
- **Other:** [blog, podcast, conference talks, publications if found]

#### Recent News & Activity
- [Bullet: recent company news or announcement involving them]
- [Bullet: article they wrote, talk they gave, award, or milestone]

#### Conversation Starters
1. **[Topic]** — "[Specific opener referencing their recent post, article, or activity]"
2. **[Topic]** — "[Opener referencing their career background or a shared professional interest]"
3. **[Topic]** — "[Opener tied to their company news or industry trend they've engaged with]"
4. **[Topic]** — "[Lighter opener based on a hobby, interest, or personal project if available]"

---

### Step 6: Confidence Flags

- Flag unverified information or ambiguous results (common names, limited public presence)
- Note if LinkedIn/Twitter profiles are unconfirmed matches
- Suggest verifying key facts before the meeting when the profile is sparse

## Tips

- Keep conversation starters specific — avoid generic openers like "I see you work in tech"
- For multiple external attendees from the same company, lead with the most senior person
- If meeting description or title reveals context (demo, QBR, intro call), tailor the briefing tone accordingly
