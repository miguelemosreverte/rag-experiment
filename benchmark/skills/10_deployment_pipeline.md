# Deployment Pipeline Tool

## Description
Manages application deployments across environments: staging, production, and canary. Integrates with Git for version tracking, runs automated tests, builds Docker containers, and deploys to Kubernetes clusters. Sends deployment notifications via Slack and email. Monitors post-deployment health metrics.

## Parameters
- `action` (required): One of "deploy", "rollback", "status", "promote", "canary".
- `service` (required): Service name as defined in the deployment manifest.
- `environment` (required): "staging", "production", or "canary".
- `version` (optional): Git tag or commit hash. Default: latest on main branch.
- `notify` (optional): Send deployment notifications. Default: true.

## Deployment Flow
```python
# 1. Deploy to staging
deploy(action="deploy", service="api-server", environment="staging", version="v2.3.1")
# Runs: git checkout → tests → docker build → k8s apply → health check

# 2. Check staging health
status = deploy(action="status", service="api-server", environment="staging")
# Returns: {"replicas": "3/3", "health": "healthy", "uptime": "2h", "error_rate": "0.01%"}

# 3. Promote to production
deploy(action="promote", service="api-server", environment="production")

# 4. If something goes wrong
deploy(action="rollback", service="api-server", environment="production")
```

## Canary Deployments
```python
# Deploy to 10% of production traffic
deploy(action="canary", service="api-server", environment="production",
       version="v2.3.2", canary_percent=10)

# Monitor canary metrics
status = deploy(action="status", service="api-server", environment="canary")
# Returns: {"canary_percent": 10, "error_rate": "0.02%", "latency_p99": "120ms"}

# Promote canary to full production
deploy(action="promote", service="api-server", environment="production")
```

## Pre-deployment Checks
- Git working directory must be clean
- All tests must pass (runs `pytest` and `cargo test` as applicable)
- Docker image must build successfully
- Database migrations are applied before deployment
- Rollback plan is generated automatically

## Notifications
Deployment events are sent to:
- Slack: `#deployments` channel with status updates
- Email: on-call engineer for production deployments
- PagerDuty: on failure or rollback

## Health Monitoring
Post-deployment, the tool monitors for 15 minutes:
- HTTP error rate (threshold: 1%)
- Response latency p99 (threshold: 500ms)
- CPU and memory usage
- Active connections
If thresholds are exceeded, automatic rollback is triggered.
