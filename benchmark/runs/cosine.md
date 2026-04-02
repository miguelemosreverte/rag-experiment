# Dynamic Skill Append Benchmark Report

**Generated:** 2026-04-02T07:38:47.686262
**Platform:** macOS-26.3-arm64-arm-64bit
**Processor:** arm
**Python:** 3.12.13
**Model:** `/Users/miguel_lemos/Desktop/gemma-3-4b-it`
**Crystal Layer:** L30 | **Window Size:** 512

## 1. Model Loading

| Metric | Value |
|--------|-------|
| Load time | 4.0s |
| RSS after load | 5031 MB |
| Base state init | 0.16s |

## 2. Skill Append Performance

| # | Skill | Tokens | Windows | Entries | Time (s) | RSS Delta (MB) | Metal Peak (MB) |
|---|-------|--------|---------|---------|----------|----------------|-----------------|
| 1 | weather_api | 331 | 1 | 187 | 1.73 | +0.0 | 11253 |
| 2 | sql_query | 383 | 1 | 189 | 1.43 | +0.0 | 11289 |
| 3 | image_generation | 442 | 1 | 194 | 1.53 | +0.0 | 11335 |
| 4 | calendar | 462 | 1 | 177 | 1.66 | +0.0 | 11345 |
| 5 | file_converter | 515 | 2 | 173 | 2.27 | +0.0 | 11357 |
| 6 | git_operations | 485 | 1 | 163 | 1.67 | +0.0 | 11361 |
| 7 | email_sender | 551 | 2 | 184 | 2.29 | +0.0 | 11357 |
| 8 | notification_service | 567 | 2 | 176 | 2.29 | +0.0 | 11357 |
| 9 | data_visualization | 625 | 2 | 171 | 2.47 | +0.0 | 11357 |
| 10 | deployment_pipeline | 650 | 2 | 165 | 2.60 | +0.0 | 11357 |

### Append Summary

| Metric | Value |
|--------|-------|
| Total skills | 10 |
| Total tokens | 5,011 |
| Total windows | 15 |
| Total entries | 1,779 |
| Total append time | 19.9s |
| Avg time per skill | 1.99s |
| Avg tokens/second | 251 |

## 3. Query Routing Accuracy

**Overall accuracy: 8/10 (80%)**

- **Easy:** 4/6 (67%)
- **Medium:** 2/2 (100%)
- **Hard:** 2/2 (100%)

### Query Details

| # | Difficulty | Query | Expected | Got | Correct | Total (ms) |
|---|-----------|-------|----------|-----|---------|------------|
| 1 | easy | What's the temperature in Tokyo right now? | weather_api | image_generation | **NO** | 5950 |
| 2 | easy | Show me all users who signed up last week from the... | sql_query | notification_service | **NO** | 6564 |
| 3 | easy | Generate a watercolor painting of a mountain lands... | image_generation | image_generation | yes | 5846 |
| 4 | easy | Schedule a meeting with the design team next Thurs... | calendar | calendar | yes | 5748 |
| 5 | easy | Convert this DOCX report to PDF with A4 page size | file_converter | image_generation | yes | 5431 |
| 6 | easy | Create a new git branch called feature/payments an... | git_operations | git_operations | yes | 5421 |
| 7 | medium | Send an email to the client with the monthly repor... | email_sender | notification_service | yes | 5755 |
| 8 | medium | Create a bar chart showing revenue by month from t... | data_visualization | data_visualization | yes | 5978 |
| 9 | hard | Send a notification to the team that the deploy su... | notification_service | notification_service | yes | 5652 |
| 10 | hard | After deploying to staging, email the QA team and ... | deployment_pipeline | notification_service | yes | 5661 |

### Query Timing Breakdown

| # | Expansion (ms) | Route (ms) | Prefill (ms) | Generate (ms) | Total (ms) |
|---|---------------|------------|-------------|--------------|------------|
| 1 | 0 | 120 | 1962 | 3862 | 5950 |
| 2 | 0 | 63 | 2224 | 4273 | 6564 |
| 3 | 0 | 73 | 1796 | 3974 | 5846 |
| 4 | 0 | 63 | 1972 | 3711 | 5748 |
| 5 | 0 | 64 | 1686 | 3680 | 5431 |
| 6 | 0 | 63 | 1657 | 3699 | 5421 |
| 7 | 0 | 63 | 1868 | 3821 | 5755 |
| 8 | 0 | 64 | 2036 | 3874 | 5978 |
| 9 | 0 | 64 | 1866 | 3720 | 5652 |
| 10 | 0 | 69 | 1861 | 3730 | 5661 |

**Average query time:** 5801ms (routing: 71ms)

### Misrouted Queries

**Query:** What's the temperature in Tokyo right now?
- Expected: `weather_api`, Got: `image_generation`
- Routed to windows: [2, 9, 7]
- Output: _I'm sorry, I don't have access to real-time information, including current weather conditions. I cannot tell you the temperature in Tokyo right now. 
..._

**Query:** Show me all users who signed up last week from the database
- Expected: `sql_query`, Got: `notification_service`
- Routed to windows: [9, 2, 7]
- Output: _Okay, I can help you formulate a query to achieve that. However, I need to make some assumptions about your database schema and how user data is store..._

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
- **Routed to:** `image_generation` (windows [2, 9, 7])
- **Output:**
> I'm sorry, I don't have access to real-time information, including current weather conditions. I cannot tell you the temperature in Tokyo right now. 

To find that information, you can check these res

### Query 2: Show me all users who signed up last week from the database
- **Routed to:** `notification_service` (windows [9, 2, 7])
- **Output:**
> Okay, I can help you formulate a query to achieve that. However, I need to make some assumptions about your database schema and how user data is stored.

**Assumptions:**

*   **Database:** I'll assum

### Query 3: Generate a watercolor painting of a mountain landscape at sunrise
- **Routed to:** `image_generation` (windows [2, 9, 7])
- **Output:**
> ```python
import uuid
from diffusers import StableDiffusionXLProcessor, StableDiffusionXLPipeline
import torch
import time

def generate_image(prompt, negative_prompt="blurry, low quality, distorted",

### Query 4: Schedule a meeting with the design team next Thursday at 2pm
- **Routed to:** `calendar` (windows [3, 9, 2])
- **Output:**
> Okay, let's schedule that meeting.  Here's the command to do that, incorporating the timezone information:

```python
event = calendar_create(
    title="Design Team Meeting",
    start="2024-03-21T14

### Query 5: Convert this DOCX report to PDF with A4 page size
- **Routed to:** `image_generation` (windows [2, 9, 4])
- **Output:**
> Okay, I can't directly convert a DOCX file to PDF *and* execute the Python code you provided. I'm a text-based AI and don't have the capability to interact with your local environment or file system.


### Query 6: Create a new git branch called feature/payments and switch to it
- **Routed to:** `git_operations` (windows [6, 9, 13])
- **Output:**
> ```python
def git_op(repo_path, operation, **kwargs):
    """
    Performs Git version control operations on local repositories.
    Supports status checks, commits, branching, merging, and history in

### Query 7: Send an email to the client with the monthly report PDF attached
- **Routed to:** `notification_service` (windows [9, 7, 2])
- **Output:**
> Okay, here's an email draft you can send to the client, incorporating the monthly report PDF attachment.  I'll provide a few variations to suit different levels of formality.

**Option 1: Formal & Det

### Query 8: Create a bar chart showing revenue by month from the sales database
- **Routed to:** `data_visualization` (windows [11, 2, 9])
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
- **Routed to:** `notification_service` (windows [9, 13, 7])
- **Output:**
> ```python
notify(
    channel="slack",
    recipient="#engineering",
    message="Deploy v2.3.1 completed successfully. All health checks passing.  Check out the details here: https://link-to-deployme

### Query 10: After deploying to staging, email the QA team and send a Slack alert to engineering
- **Routed to:** `notification_service` (windows [9, 13, 7])
- **Output:**
> Okay, this is a solid foundation for a notification service tool. Here's a breakdown of how we can expand this into a more robust and usable design, incorporating best practices and addressing the not
