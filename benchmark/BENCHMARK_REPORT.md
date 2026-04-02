# Dynamic Skill Append Benchmark Report

**Generated:** 2026-04-02T06:51:06.132700
**Platform:** macOS-26.3-arm64-arm-64bit
**Processor:** arm
**Python:** 3.12.13
**Model:** `/Users/miguel_lemos/Desktop/gemma-3-4b-it`
**Crystal Layer:** L30 | **Window Size:** 512

## 1. Model Loading

| Metric | Value |
|--------|-------|
| Load time | 3.4s |
| RSS after load | 5177 MB |
| Base state init | 0.14s |

## 2. Skill Append Performance

| # | Skill | Tokens | Windows | Entries | Time (s) | RSS Delta (MB) | Metal Peak (MB) |
|---|-------|--------|---------|---------|----------|----------------|-----------------|
| 1 | weather_api | 331 | 1 | 187 | 1.46 | +0.0 | 11253 |
| 2 | sql_query | 383 | 1 | 189 | 1.48 | +0.0 | 11289 |
| 3 | image_generation | 442 | 1 | 194 | 1.56 | +0.0 | 11335 |
| 4 | calendar | 462 | 1 | 177 | 1.68 | +0.0 | 11345 |
| 5 | file_converter | 515 | 2 | 173 | 2.28 | +0.0 | 11357 |
| 6 | git_operations | 485 | 1 | 163 | 1.70 | +0.0 | 11361 |
| 7 | email_sender | 551 | 2 | 184 | 2.33 | +0.0 | 11357 |
| 8 | notification_service | 567 | 2 | 176 | 2.33 | +0.0 | 11357 |
| 9 | data_visualization | 625 | 2 | 171 | 2.49 | +0.0 | 11357 |
| 10 | deployment_pipeline | 650 | 2 | 165 | 2.63 | +0.0 | 11357 |

### Append Summary

| Metric | Value |
|--------|-------|
| Total skills | 10 |
| Total tokens | 5,011 |
| Total windows | 15 |
| Total entries | 1,779 |
| Total append time | 19.9s |
| Avg time per skill | 1.99s |
| Avg tokens/second | 252 |

## 3. Query Routing Accuracy

**Overall accuracy: 8/10 (80%)**

- **Easy:** 5/6 (83%)
- **Medium:** 2/2 (100%)
- **Hard:** 1/2 (50%)

### Query Details

| # | Difficulty | Query | Expected | Got | Correct | Total (ms) |
|---|-----------|-------|----------|-----|---------|------------|
| 1 | easy | What's the temperature in Tokyo right now? | weather_api | calendar | **NO** | 6976 |
| 2 | easy | Show me all users who signed up last week from the... | sql_query | sql_query | yes | 6731 |
| 3 | easy | Generate a watercolor painting of a mountain lands... | image_generation | image_generation | yes | 6708 |
| 4 | easy | Schedule a meeting with the design team next Thurs... | calendar | calendar | yes | 6985 |
| 5 | easy | Convert this DOCX report to PDF with A4 page size | file_converter | file_converter | yes | 7122 |
| 6 | easy | Create a new git branch called feature/payments an... | git_operations | git_operations | yes | 6892 |
| 7 | medium | Send an email to the client with the monthly repor... | email_sender | email_sender | yes | 7165 |
| 8 | medium | Create a bar chart showing revenue by month from t... | data_visualization | data_visualization | yes | 7215 |
| 9 | hard | Send a notification to the team that the deploy su... | notification_service | deployment_pipeline | **NO** | 6867 |
| 10 | hard | After deploying to staging, email the QA team and ... | deployment_pipeline | deployment_pipeline | yes | 6934 |

### Query Timing Breakdown

| # | Expansion (ms) | Route (ms) | Prefill (ms) | Generate (ms) | Total (ms) |
|---|---------------|------------|-------------|--------------|------------|
| 1 | 1126 | 0 | 1818 | 4027 | 6976 |
| 2 | 1143 | 0 | 1790 | 3795 | 6731 |
| 3 | 1136 | 0 | 1738 | 3833 | 6708 |
| 4 | 1159 | 0 | 1907 | 3917 | 6985 |
| 5 | 1134 | 0 | 2097 | 3888 | 7122 |
| 6 | 1157 | 0 | 1853 | 3880 | 6892 |
| 7 | 1187 | 0 | 2040 | 3936 | 7165 |
| 8 | 1142 | 0 | 2176 | 3895 | 7215 |
| 9 | 1140 | 0 | 1915 | 3810 | 6867 |
| 10 | 1148 | 1 | 1902 | 3881 | 6934 |

**Average query time:** 6959ms (routing: 0ms)

### Misrouted Queries

**Query:** What's the temperature in Tokyo right now?
- Expected: `weather_api`, Got: `calendar`
- Routed to windows: [3, 9]
- Output: _I am sorry, I cannot provide you with the current temperature in Tokyo. I am a language model and do not have access to real-time weather data. 

To f..._

**Query:** Send a notification to the team that the deploy succeeded and include a link
- Expected: `notification_service`, Got: `deployment_pipeline`
- Routed to windows: [13, 9, 12]
- Output: _Okay, here's a Python implementation of the Deployment Pipeline Tool, incorporating the described functionality, parameters, deployment flow, canary d..._

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
- **Routed to:** `calendar` (windows [3, 9])
- **Output:**
> I am sorry, I cannot provide you with the current temperature in Tokyo. I am a language model and do not have access to real-time weather data. 

To find the current temperature in Tokyo, you can use 

### Query 2: Show me all users who signed up last week from the database
- **Routed to:** `sql_query` (windows [1, 11, 2])
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
- **Routed to:** `image_generation` (windows [2, 9])
- **Output:**
> ```python
import uuid
from diffusers import StableDiffusionXLProcessor, StableDiffusionXLPipeline
import torch
import time

def generate_image(prompt, negative_prompt="blurry, low quality, distorted",

### Query 4: Schedule a meeting with the design team next Thursday at 2pm
- **Routed to:** `calendar` (windows [3, 1, 2])
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
- **Routed to:** `git_operations` (windows [6, 13, 4])
- **Output:**
> ```python
def git_op(repo_path, operation, **kwargs):
    """
    Performs Git version control operations on local repositories.
    Supports status checks, commits, branching, merging, and history in

### Query 7: Send an email to the client with the monthly report PDF attached
- **Routed to:** `email_sender` (windows [7, 4, 9])
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
- **Routed to:** `data_visualization` (windows [11, 1, 12])
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
- **Routed to:** `deployment_pipeline` (windows [13, 9, 12])
- **Output:**
> Okay, here's a Python implementation of the Deployment Pipeline Tool, incorporating the described functionality, parameters, deployment flow, canary deployments, and pre-deployment checks.  I've focus

### Query 10: After deploying to staging, email the QA team and send a Slack alert to engineering
- **Routed to:** `deployment_pipeline` (windows [13, 9, 1])
- **Output:**
> Okay, this is a solid foundation for a deployment pipeline tool. Let's flesh this out into a more detailed Python implementation, incorporating the described features and considerations.  This will be
