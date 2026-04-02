# Dynamic Skill Append Benchmark Report

**Generated:** 2026-04-02T07:14:37.559741
**Platform:** macOS-26.3-arm64-arm-64bit
**Processor:** arm
**Python:** 3.12.13
**Model:** `/Users/miguel_lemos/Desktop/gemma-3-4b-it`
**Crystal Layer:** L30 | **Window Size:** 512

## 1. Model Loading

| Metric | Value |
|--------|-------|
| Load time | 3.3s |
| RSS after load | 5741 MB |
| Base state init | 0.15s |

## 2. Skill Append Performance

| # | Skill | Tokens | Windows | Entries | Time (s) | RSS Delta (MB) | Metal Peak (MB) |
|---|-------|--------|---------|---------|----------|----------------|-----------------|
| 1 | weather_api | 331 | 1 | 187 | 1.50 | +0.0 | 11253 |
| 2 | sql_query | 383 | 1 | 189 | 1.53 | +0.0 | 11289 |
| 3 | image_generation | 442 | 1 | 194 | 1.65 | +0.0 | 11335 |
| 4 | calendar | 462 | 1 | 177 | 1.73 | +0.0 | 11345 |
| 5 | file_converter | 515 | 2 | 173 | 2.38 | +0.0 | 11357 |
| 6 | git_operations | 485 | 1 | 163 | 1.71 | +0.0 | 11361 |
| 7 | email_sender | 551 | 2 | 184 | 2.34 | +0.0 | 11357 |
| 8 | notification_service | 567 | 2 | 176 | 2.37 | +0.0 | 11357 |
| 9 | data_visualization | 625 | 2 | 171 | 2.54 | +0.0 | 11357 |
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

**Overall accuracy: 9/10 (90%)**

- **Easy:** 6/6 (100%)
- **Medium:** 2/2 (100%)
- **Hard:** 1/2 (50%)

### Query Details

| # | Difficulty | Query | Expected | Got | Correct | Total (ms) |
|---|-----------|-------|----------|-----|---------|------------|
| 1 | easy | What's the temperature in Tokyo right now? | weather_api | weather_api | yes | 6460 |
| 2 | easy | Show me all users who signed up last week from the... | sql_query | sql_query | yes | 7261 |
| 3 | easy | Generate a watercolor painting of a mountain lands... | image_generation | image_generation | yes | 7322 |
| 4 | easy | Schedule a meeting with the design team next Thurs... | calendar | calendar | yes | 7295 |
| 5 | easy | Convert this DOCX report to PDF with A4 page size | file_converter | file_converter | yes | 7348 |
| 6 | easy | Create a new git branch called feature/payments an... | git_operations | git_operations | yes | 6950 |
| 7 | medium | Send an email to the client with the monthly repor... | email_sender | email_sender | yes | 7028 |
| 8 | medium | Create a bar chart showing revenue by month from t... | data_visualization | data_visualization | yes | 7014 |
| 9 | hard | Send a notification to the team that the deploy su... | notification_service | notification_service | yes | 7148 |
| 10 | hard | After deploying to staging, email the QA team and ... | deployment_pipeline | notification_service | **NO** | 7473 |

### Query Timing Breakdown

| # | Expansion (ms) | Route (ms) | Prefill (ms) | Generate (ms) | Total (ms) |
|---|---------------|------------|-------------|--------------|------------|
| 1 | 1127 | 3 | 1438 | 3883 | 6460 |
| 2 | 1133 | 0 | 2060 | 4061 | 7261 |
| 3 | 1156 | 0 | 2206 | 3955 | 7322 |
| 4 | 1135 | 0 | 2095 | 4059 | 7295 |
| 5 | 1129 | 0 | 2354 | 3860 | 7348 |
| 6 | 1188 | 0 | 1957 | 3799 | 6950 |
| 7 | 1124 | 0 | 2104 | 3794 | 7028 |
| 8 | 1128 | 0 | 2062 | 3819 | 7014 |
| 9 | 1172 | 0 | 2193 | 3777 | 7148 |
| 10 | 1153 | 0 | 2458 | 3857 | 7473 |

**Average query time:** 7130ms (routing: 0ms)

### Misrouted Queries

**Query:** After deploying to staging, email the QA team and send a Slack alert to engineering
- Expected: `deployment_pipeline`, Got: `notification_service`
- Routed to windows: [9, 13]
- Output: _Okay, this is a solid foundation for a notification service tool. Here's a breakdown of how we can expand this into a more robust and usable design, i..._

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
- **Routed to:** `git_operations` (windows [6, 13])
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
