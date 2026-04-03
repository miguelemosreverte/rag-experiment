# Dynamic Skill Append Benchmark Report

**Generated:** 2026-04-03T13:01:18.980272
**Platform:** macOS-26.3-arm64-arm-64bit
**Processor:** arm
**Python:** 3.12.13
**Model:** `/Users/miguel_lemos/Desktop/gemma-3-4b-it`
**Crystal Layer:** L30 | **Window Size:** 512

## 1. Model Loading

| Metric | Value |
|--------|-------|
| Load time | 5.1s |
| RSS after load | 970 MB |
| Base state init | 0.25s |

## 2. Skill Append Performance

| # | Skill | Tokens | Windows | Entries | Time (s) | RSS Delta (MB) | Metal Peak (MB) |
|---|-------|--------|---------|---------|----------|----------------|-----------------|
| 1 | weather_api | 331 | 1 | 187 | 87.24 | +7180.2 | 11253 |
| 2 | sql_query | 383 | 1 | 189 | 47.65 | +27.1 | 11289 |
| 3 | image_generation | 442 | 1 | 194 | 25.02 | +0.0 | 11335 |
| 4 | calendar | 462 | 1 | 177 | 25.76 | +0.0 | 11345 |
| 5 | file_converter | 515 | 2 | 173 | 25.75 | +0.0 | 11357 |
| 6 | git_operations | 485 | 1 | 163 | 25.09 | +0.0 | 11361 |
| 7 | email_sender | 551 | 2 | 184 | 26.36 | +0.0 | 11357 |
| 8 | notification_service | 567 | 2 | 176 | 27.61 | +0.0 | 11357 |
| 9 | data_visualization | 625 | 2 | 171 | 28.23 | +0.0 | 11357 |
| 10 | deployment_pipeline | 650 | 2 | 165 | 29.63 | +0.0 | 11357 |

### Append Summary

| Metric | Value |
|--------|-------|
| Total skills | 10 |
| Total tokens | 5,011 |
| Total windows | 15 |
| Total entries | 1,779 |
| Total append time | 348.3s |
| Avg time per skill | 34.83s |
| Avg tokens/second | 14 |

## 3. Query Routing Accuracy

**Overall accuracy: 7/10 (70%)**

- **Easy:** 5/6 (83%)
- **Medium:** 1/2 (50%)
- **Hard:** 1/2 (50%)

### Query Details

| # | Difficulty | Query | Expected | Got | Correct | Total (ms) |
|---|-----------|-------|----------|-----|---------|------------|
| 1 | easy | What's the temperature in Tokyo right now? | weather_api | weather_api | yes | 11805 |
| 2 | easy | Show me all users who signed up last week from the... | sql_query | sql_query | yes | 7035 |
| 3 | easy | Generate a watercolor painting of a mountain lands... | image_generation | image_generation | yes | 6150 |
| 4 | easy | Schedule a meeting with the design team next Thurs... | calendar | calendar | yes | 6038 |
| 5 | easy | Convert this DOCX report to PDF with A4 page size | file_converter | file_converter | yes | 4879 |
| 6 | easy | Create a new git branch called feature/payments an... | git_operations | image_generation | **NO** | 6536 |
| 7 | medium | Send an email to the client with the monthly repor... | email_sender | notification_service | **NO** | 4609 |
| 8 | medium | Create a bar chart showing revenue by month from t... | data_visualization | data_visualization | yes | 5387 |
| 9 | hard | Send a notification to the team that the deploy su... | notification_service | image_generation | yes | 6608 |
| 10 | hard | After deploying to staging, email the QA team and ... | deployment_pipeline | notification_service | **NO** | 4868 |

### Query Timing Breakdown

| # | Expansion (ms) | Route (ms) | Prefill (ms) | Generate (ms) | Total (ms) |
|---|---------------|------------|-------------|--------------|------------|
| 1 | 0 | 2889 | 4958 | 3940 | 11805 |
| 2 | 0 | 1323 | 1735 | 3944 | 7035 |
| 3 | 0 | 278 | 1800 | 4068 | 6150 |
| 4 | 0 | 274 | 1860 | 3898 | 6038 |
| 5 | 0 | 243 | 426 | 4206 | 4879 |
| 6 | 0 | 259 | 2012 | 4261 | 6536 |
| 7 | 0 | 195 | 607 | 3800 | 4609 |
| 8 | 0 | 328 | 1181 | 3869 | 5387 |
| 9 | 0 | 292 | 1991 | 4321 | 6608 |
| 10 | 0 | 334 | 718 | 3814 | 4868 |

**Average query time:** 6391ms (routing: 641ms)

### Misrouted Queries

**Query:** Create a new git branch called feature/payments and switch to it
- Expected: `git_operations`, Got: `image_generation`
- Routed to windows: [2, 12, 11]
- Output: _Okay, I've created a new Git branch called `feature/payments` and switched to it.

Here's the command I executed to do that (assuming you're using a s..._

**Query:** Send an email to the client with the monthly report PDF attached
- Expected: `email_sender`, Got: `notification_service`
- Routed to windows: [10, 9, 2]
- Output: _Okay, here's a draft email to the client, incorporating the rate limits and attaching the monthly report PDF.  I've aimed for a professional and infor..._

**Query:** After deploying to staging, email the QA team and send a Slack alert to engineering
- Expected: `deployment_pipeline`, Got: `notification_service`
- Routed to windows: [10, 9, 2]
- Output: _Okay, let's break down this task and create a plan with code snippets (primarily Python, as it's a common choice for automation) to achieve the desire..._

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
- **Routed to:** `weather_api` (windows [0, 3, 10])
- **Output:**
> ```tool_code
weather = get_weather(city="Tokyo")
print(weather)
```

### Query 2: Show me all users who signed up last week from the database
- **Routed to:** `sql_query` (windows [1, 3, 2])
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
- **Routed to:** `image_generation` (windows [2, 12, 11])
- **Output:**
> ```python
import uuid
from diffusers import StableDiffusionXLProcessor, StableDiffusionXLPipeline
import torch
import time

def generate_image(prompt, negative_prompt="blurry, low quality, distorted",

### Query 4: Schedule a meeting with the design team next Thursday at 2pm
- **Routed to:** `calendar` (windows [3, 2, 10])
- **Output:**
> Okay, let's schedule that meeting.  Here's the command to do that, incorporating the timezone information:

```python
event = calendar_create(
    title="Design Team Meeting",
    start="2024-03-21T14

### Query 5: Convert this DOCX report to PDF with A4 page size
- **Routed to:** `file_converter` (windows [5, 4, 10])
- **Output:**
> Please provide me with the DOCX report! I need the file itself to be able to convert it to PDF with A4 page size. 

You can do this by:

* **Uploading the file directly to our chat.** (If the platform

### Query 6: Create a new git branch called feature/payments and switch to it
- **Routed to:** `image_generation` (windows [2, 12, 11])
- **Output:**
> Okay, I've created a new Git branch called `feature/payments` and switched to it.

Here's the command I executed to do that (assuming you're using a standard Git setup):

```bash
git checkout -b featu

### Query 7: Send an email to the client with the monthly report PDF attached
- **Routed to:** `notification_service` (windows [10, 9, 2])
- **Output:**
> Okay, here's a draft email to the client, incorporating the rate limits and attaching the monthly report PDF.  I've aimed for a professional and informative tone.

**Subject: Monthly Report - [Client 

### Query 8: Create a bar chart showing revenue by month from the sales database
- **Routed to:** `data_visualization` (windows [12, 11, 2])
- **Output:**
> ```python
import pandas as pd
import plotly.express as px

def create_revenue_by_month_bar_chart(sales_data):
    """
    Creates an interactive bar chart showing revenue by month from sales data.

  

### Query 9: Send a notification to the team that the deploy succeeded and include a link
- **Routed to:** `image_generation` (windows [2, 10, 9])
- **Output:**
> Okay, here's a notification message for the team, including a link, confirming the successful deployment of the Image Generation Tool:

Subject: 🎉 Image Generation Tool Deployed Successfully! 🎉

Hi Te

### Query 10: After deploying to staging, email the QA team and send a Slack alert to engineering
- **Routed to:** `notification_service` (windows [10, 9, 2])
- **Output:**
> Okay, let's break down this task and create a plan with code snippets (primarily Python, as it's a common choice for automation) to achieve the desired outcome.

**1. Understanding the Requirements**

