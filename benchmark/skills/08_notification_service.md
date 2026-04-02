# Notification Service Tool

## Description
Sends notifications across multiple channels: push notifications (iOS/Android via Firebase), SMS (via Twilio), email (via SendGrid), and Slack messages. Supports scheduling, batching, and delivery tracking. This is the unified notification hub — use it when you need to reach users through their preferred channel.

## Parameters
- `channel` (required): One of "push", "sms", "email", "slack".
- `recipient` (required): User ID, phone number, email address, or Slack channel.
- `message` (required): Notification content (plain text).
- `title` (optional): Notification title (for push/email).
- `priority` (optional): "low", "normal", "high", "critical". Default: "normal".
- `schedule_at` (optional): ISO 8601 datetime to send later.
- `template_id` (optional): Pre-defined template ID for consistent formatting.

## Example Usage
```python
notify(
    channel="email",
    recipient="user@example.com",
    title="Your Order Has Shipped",
    message="Your order #12345 is on its way. Track it at: https://track.example.com/12345",
    priority="high"
)

notify(
    channel="slack",
    recipient="#engineering",
    message="Deploy v2.3.1 completed successfully. All health checks passing.",
    priority="normal"
)
```

## Delivery Tracking
```python
status = notification_status(notification_id="notif_abc123")
# Returns: {"status": "delivered", "channel": "email", "delivered_at": "...", "opened": true}
```

## Templates
Pre-defined templates for common notifications: welcome_email, password_reset, order_confirmation, shipping_update, payment_receipt. Templates support variable substitution with `{{variable}}` syntax.

## Channel-Specific Notes
- **Push**: Requires device token. Falls back to email if token expired.
- **SMS**: 160 character limit. Longer messages split into segments.
- **Email**: Supports HTML via templates. Plain text for ad-hoc messages.
- **Slack**: Supports Block Kit formatting. Threads supported via `thread_ts`.

## Rate Limits
- Push: 1000/second
- SMS: 100/second (Twilio limit)
- Email: 1000/hour (SendGrid)
- Slack: 1 message/second per channel
