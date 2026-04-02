# Calendar Management Tool

## Description
Manages Google Calendar events — create, read, update, and delete meetings and appointments. Supports multiple calendars, recurring events, and timezone-aware scheduling.

## Authentication
OAuth2 with Google Calendar API. Credentials stored in `~/.config/calendar/credentials.json`. Requires scopes: `calendar.events`, `calendar.readonly`.

## Commands

### List Events
```python
events = calendar_list(
    start="2024-03-01T00:00:00",
    end="2024-03-07T23:59:59",
    calendar_id="primary"
)
```

### Create Event
```python
event = calendar_create(
    title="Team Standup",
    start="2024-03-15T09:00:00",
    end="2024-03-15T09:30:00",
    timezone="America/Los_Angeles",
    attendees=["alice@company.com", "bob@company.com"],
    recurrence="RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR",
    description="Daily sync on sprint progress",
    location="Zoom: https://zoom.us/j/123456"
)
```

### Update Event
```python
calendar_update(event_id="abc123", title="Updated Standup", start="2024-03-15T09:30:00")
```

### Delete Event
```python
calendar_delete(event_id="abc123")
```

## Conflict Detection
When creating events, the tool checks for conflicts with existing events and warns if there's an overlap. Use `force=True` to create anyway.

## Timezone Handling
All times are converted to UTC internally. Display times use the calendar's default timezone unless overridden. The tool understands natural language like "next Tuesday at 3pm PST".
