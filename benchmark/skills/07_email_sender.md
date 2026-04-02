# Email Sender Tool

## Description
Sends emails via SMTP with support for HTML bodies, attachments, CC/BCC, and templates. Uses the configured SMTP server (Gmail, SendGrid, or custom). Supports bulk sending with rate limiting and personalization via Jinja2 templates.

## Configuration
Environment variables:
- `SMTP_HOST`: SMTP server hostname (default: smtp.gmail.com)
- `SMTP_PORT`: SMTP port (default: 587 for TLS)
- `SMTP_USER`: Authentication username
- `SMTP_PASSWORD`: Authentication password or app-specific password

## Parameters
- `to` (required): Recipient email address or list of addresses.
- `subject` (required): Email subject line.
- `body` (required): Email body (plain text or HTML).
- `html` (optional): If true, body is treated as HTML. Default: false.
- `cc` (optional): CC recipients.
- `bcc` (optional): BCC recipients.
- `attachments` (optional): List of file paths to attach.
- `reply_to` (optional): Reply-to address.

## Example Usage
```python
send_email(
    to="client@example.com",
    subject="Monthly Report - March 2024",
    body="<h1>Monthly Report</h1><p>Please find the report attached.</p>",
    html=True,
    attachments=["/reports/march_2024.pdf"],
    cc=["manager@company.com"]
)
# Returns: {"message_id": "<abc123@gmail.com>", "status": "sent", "timestamp": "..."}
```

## Templating
```python
send_email(
    to=["alice@co.com", "bob@co.com"],
    subject="Hello {{name}}",
    body="Dear {{name}}, your account balance is {{balance}}.",
    template_data=[
        {"name": "Alice", "balance": "$1,234"},
        {"name": "Bob", "balance": "$5,678"}
    ]
)
```

## Rate Limiting
- Gmail: 500 emails/day
- SendGrid: based on plan
- Custom: configurable via `SMTP_RATE_LIMIT` (emails per minute)

## Limitations
- Maximum attachment size: 25MB total
- Maximum recipients per email: 100
- HTML emails are sanitized to prevent XSS in email clients
