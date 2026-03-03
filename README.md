# client-meeting-researcher

A [Claude Code](https://claude.ai/claude-code) skill that prepares you for client meetings by automatically researching external attendees from your Google Calendar.

## What it does

1. **Fetches your upcoming meetings** from Google Calendar
2. **Identifies external attendees** (anyone outside your company domain)
3. **Researches each person online** — LinkedIn, Twitter/X, news, publications
4. **Generates a pre-meeting briefing** with professional background, online presence, and recent activity
5. **Suggests conversation starters** tailored to each person's interests and background

## Example output

```
## Pre-Meeting Briefing: Q2 Partnership Sync
Date: Monday March 9, 2026 at 2:00 PM | Duration: 45 min

### Jane Smith
Title: VP of Product at Acme Corp
Email: jane@acme.com

#### Professional Background
Jane has spent 10 years in B2B SaaS, most recently leading product at Acme Corp
where she oversees a team of 20. Previously at Salesforce and HubSpot.

#### Online Presence
- LinkedIn: linkedin.com/in/janesmith — 4,200 followers
  - Recent focus: AI in enterprise workflows, product-led growth
- Twitter/X: @janesmith — 1,800 followers
  - Engages with: startup ops, product strategy

#### Conversation Starters
1. **AI in product** — "I saw your post on AI copilots in enterprise — are you experimenting with that at Acme?"
2. **PLG transition** — "Acme's move toward self-serve looked interesting — how has that shifted your roadmap priorities?"
```

## Installation

### 1. Install dependencies

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 2. Set up Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable the **Google Calendar API**
3. Go to **APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID** (Desktop App)
4. Download the JSON and save it as:
   ```
   ~/.claude/skills/client-meeting-researcher/credentials.json
   ```
5. Run the fetch script once to authorize — a browser window opens and `token.json` is saved automatically

### 3. Install the skill in Claude Code

Copy the skill folder into your Claude skills directory:

```bash
cp -r . ~/.claude/skills/client-meeting-researcher
```

## Usage

Trigger the skill by asking Claude:

- *"Prep me for my client meetings this week"*
- *"Who am I meeting with tomorrow? Give me a briefing"*
- *"Research the external attendees in my calendar for the next 3 days"*

Claude will ask for your company email domain (to filter internal vs external), then run the full research workflow.

## Files

```
client-meeting-researcher/
├── SKILL.md                    # Skill instructions for Claude
└── scripts/
    └── fetch_calendar.py       # Google Calendar API fetcher
```
