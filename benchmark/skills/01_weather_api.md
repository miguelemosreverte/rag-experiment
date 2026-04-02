# Weather API Tool

## Description
Retrieves current weather conditions and 7-day forecasts for any location worldwide using the OpenWeatherMap API.

## Endpoint
`GET https://api.openweathermap.org/data/2.5/weather`

## Parameters
- `city` (required): City name, e.g. "San Francisco"
- `units` (optional): "metric" (Celsius) or "imperial" (Fahrenheit). Default: metric.
- `days` (optional): Number of forecast days, 1-7. Default: 1.

## Authentication
Requires an API key passed as `appid` query parameter. Store in environment variable `OPENWEATHER_API_KEY`.

## Example Usage
```python
weather = get_weather(city="Buenos Aires", units="metric", days=3)
# Returns: {"temp": 22, "humidity": 65, "wind_speed": 12, "condition": "partly cloudy"}
```

## Rate Limits
- Free tier: 60 calls/minute, 1,000,000 calls/month
- Paid tier: unlimited calls

## Error Handling
- 401: Invalid API key
- 404: City not found
- 429: Rate limit exceeded

## Notes
- Wind speed is returned in m/s for metric, mph for imperial.
- UV index is included in the response for current conditions.
- Precipitation probability is given as a percentage for forecasts.
