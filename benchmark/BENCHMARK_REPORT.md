# Dynamic Skill Append Benchmark Report

**Generated:** 2026-04-02T07:28:26.740846
**Platform:** macOS-26.3-arm64-arm-64bit
**Processor:** arm
**Python:** 3.12.13
**Model:** `/Users/miguel_lemos/Desktop/gemma-3-4b-it`
**Crystal Layer:** L30 | **Window Size:** 512

## 1. Model Loading

| Metric | Value |
|--------|-------|
| Load time | 3.3s |
| RSS after load | 4716 MB |
| Base state init | 0.14s |

## 2. Skill Append Performance

| # | Skill | Tokens | Windows | Entries | Time (s) | RSS Delta (MB) | Metal Peak (MB) |
|---|-------|--------|---------|---------|----------|----------------|-----------------|
| 1 | weather_api | 331 | 1 | 187 | 1.45 | +0.0 | 11253 |
| 2 | sql_query | 383 | 1 | 189 | 1.42 | +0.0 | 11289 |
| 3 | image_generation | 442 | 1 | 194 | 1.53 | +0.0 | 11335 |
| 4 | calendar | 462 | 1 | 177 | 1.66 | +0.0 | 11345 |
| 5 | file_converter | 515 | 2 | 173 | 2.24 | +0.0 | 11357 |
| 6 | git_operations | 485 | 1 | 163 | 1.79 | +0.0 | 11361 |
| 7 | email_sender | 551 | 2 | 184 | 2.60 | +0.0 | 11357 |
| 8 | notification_service | 567 | 2 | 176 | 2.54 | +0.0 | 11357 |
| 9 | data_visualization | 625 | 2 | 171 | 2.50 | +0.0 | 11357 |
| 10 | deployment_pipeline | 650 | 2 | 165 | 2.65 | +0.0 | 11357 |

### Append Summary

| Metric | Value |
|--------|-------|
| Total skills | 10 |
| Total tokens | 5,011 |
| Total windows | 15 |
| Total entries | 1,779 |
| Total append time | 20.4s |
| Avg time per skill | 2.04s |
| Avg tokens/second | 246 |

## 3. Query Routing Accuracy

**Overall accuracy: 10/10 (100%)**

- **Easy:** 6/6 (100%)
- **Medium:** 2/2 (100%)
- **Hard:** 2/2 (100%)

### Query Details

| # | Difficulty | Query | Expected | Got | Correct | Total (ms) |
|---|-----------|-------|----------|-----|---------|------------|
| 1 | easy | What's the temperature in Tokyo right now? | weather_api | weather_api | yes | 7209 |
| 2 | easy | Show me all users who signed up last week from the... | sql_query | sql_query | yes | 8015 |
| 3 | easy | Generate a watercolor painting of a mountain lands... | image_generation | image_generation | yes | 8105 |
| 4 | easy | Schedule a meeting with the design team next Thurs... | calendar | calendar | yes | 25015 |
| 5 | easy | Convert this DOCX report to PDF with A4 page size | file_converter | file_converter | yes | 13963 |
| 6 | easy | Create a new git branch called feature/payments an... | git_operations | git_operations | yes | 12627 |
| 7 | medium | Send an email to the client with the monthly repor... | email_sender | email_sender | yes | 13145 |
| 8 | medium | Create a bar chart showing revenue by month from t... | data_visualization | data_visualization | yes | 12662 |
| 9 | hard | Send a notification to the team that the deploy su... | notification_service | notification_service | yes | 17028 |
| 10 | hard | After deploying to staging, email the QA team and ... | deployment_pipeline | notification_service | yes | 30432 |

### Query Timing Breakdown

| # | Expansion (ms) | Route (ms) | Prefill (ms) | Generate (ms) | Total (ms) |
|---|---------------|------------|-------------|--------------|------------|
| 1 | 1226 | 3 | 1519 | 4453 | 7209 |
| 2 | 1329 | 0 | 2213 | 4466 | 8015 |
| 3 | 1364 | 0 | 2111 | 4624 | 8105 |
| 4 | 8213 | 1 | 8532 | 8251 | 25015 |
| 5 | 2195 | 2 | 5025 | 6693 | 13963 |
| 6 | 2233 | 1 | 3903 | 6472 | 12627 |
| 7 | 1790 | 0 | 4530 | 6806 | 13145 |
| 8 | 2001 | 0 | 4453 | 6185 | 12662 |
| 9 | 1797 | 0 | 5105 | 10114 | 17028 |
| 10 | 4441 | 0 | 6743 | 19242 | 30432 |

**Average query time:** 14820ms (routing: 1ms)

## 4. Store Statistics

| Metric | Value |
|--------|-------|
| Store version | v12 |
| Total windows | 15 |
| Total entries | 1,779 |
| IDF table size | 1,316 tokens |
| Keywords | 98 total |

## 5. Sample Query Outputs

### Query 1: What's the temperature in Tokyo right now?
- **Routed to:** `weather_api` (windows [0, 3])
- **Output:**
> ```tool_code
weather = get_weather(city="Tokyo")
print(weather)
```

### Query 2: Show me all users who signed up last week from the database
- **Routed to:** `sql_query` (windows [1, 9, 11])
- **Output:**
> ```python
import os
import logging
import json
import hashlib

from asyncpg import create_pool

logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL

### Query 3: Generate a watercolor painting of a mountain landscape at sunrise
- **Routed to:** `image_generation` (windows [2])
- **Output:**
> ```python
import uuid
from diffusers import StableDiffusionXLProcessor, StableDiffusionXLPipeline
import torch
import time

def generate_image(prompt, negative_prompt="blurry, low quality, distorted",

### Query 4: Schedule a meeting with the design team next Thursday at 2pm
- **Routed to:** `calendar` (windows [3])
- **Output:**
> Okay, let's schedule that meeting.  Here's the command to do that, incorporating the timezone information:

```python
event = calendar_create(
    title="Design Team Meeting",
    start="2024-03-21T14

### Query 5: Convert this DOCX report to PDF with A4 page size
- **Routed to:** `file_converter` (windows [4])
- **Output:**
> ```python
def convert_file(input_path, output_format, output_path=None, options=None):
    """
    Converts files between common formats using pandoc and openpyxl.

    Args:
        input_path (str):

### Query 6: Create a new git branch called feature/payments and switch to it
- **Routed to:** `git_operations` (windows [6])
- **Output:**
> ```python
def git_op(repo_path, operation, **kwargs):
    """
    Performs Git version control operations on local repositories.
    Supports status checks, commits, branching, merging, and history in

### Query 7: Send an email to the client with the monthly report PDF attached
- **Routed to:** `email_sender` (windows [7])
- **Output:**
> ```python
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from jinja2 impor

### Query 8: Create a bar chart showing revenue by month from the sales database
- **Routed to:** `data_visualization` (windows [11])
- **Output:**
> ```python
import pandas as pd
import plotly.express as px
import uuid
import os

def visualize(data, chart_type, x, y, title=None, color=None, output_format="html", output_path=None):
    """
    Crea

### Query 9: Send a notification to the team that the deploy succeeded and include a link
- **Routed to:** `notification_service` (windows [9, 13])
- **Output:**
> ```python
notify(
    channel="slack",
    recipient="#engineering",
    message="Deploy v2.3.1 completed successfully. All health checks passing.  Check out the details here: https://link-to-deployme

### Query 10: After deploying to staging, email the QA team and send a Slack alert to engineering
- **Routed to:** `notification_service` (windows [9, 13])
- **Output:**
> Okay, this is a solid foundation for a notification service tool. Here's a breakdown of how we can expand this into a more robust and usable design, incorporating best practices and addressing the not
