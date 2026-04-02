# Data Visualization Tool

## Description
Creates charts, graphs, and dashboards from structured data. Supports bar charts, line graphs, scatter plots, heatmaps, pie charts, and geographic maps. Uses Plotly for interactive HTML charts and Matplotlib for static PNG/SVG export. Can query databases directly using SQL to fetch data before visualizing it.

## Parameters
- `data` (required): Data as a list of dicts, CSV path, JSON path, or a SQL query string.
- `chart_type` (required): One of "bar", "line", "scatter", "heatmap", "pie", "map", "histogram", "box".
- `x` (required for most): Column name for x-axis.
- `y` (required for most): Column name for y-axis.
- `title` (optional): Chart title.
- `color` (optional): Column name for color grouping.
- `output_format` (optional): "html" (interactive), "png", "svg", "pdf". Default: "html".
- `output_path` (optional): Where to save. Default: `/tmp/chart_<uuid>.<format>`.

## Example Usage
```python
# From inline data
chart = visualize(
    data=[{"month": "Jan", "revenue": 50000}, {"month": "Feb", "revenue": 62000}],
    chart_type="bar",
    x="month",
    y="revenue",
    title="Monthly Revenue Q1 2024"
)

# From SQL query (connects to DATABASE_URL)
chart = visualize(
    data="SELECT date, count(*) as signups FROM users GROUP BY date ORDER BY date",
    chart_type="line",
    x="date",
    y="signups",
    title="Daily Signups",
    output_format="png"
)
```

## Dashboard Mode
```python
dashboard = create_dashboard(
    charts=[chart1, chart2, chart3],
    layout="2x2",
    title="Sales Dashboard Q1"
)
# Returns interactive HTML with all charts
```

## Geographic Maps
```python
chart = visualize(
    data="SELECT city, latitude, longitude, population FROM cities",
    chart_type="map",
    title="City Population Map",
    size="population"
)
```

## Styling
- Built-in themes: "default", "dark", "minimal", "corporate"
- Custom colors via `color_palette` parameter
- Annotations via `annotations` parameter

## Notes
- Interactive HTML charts include zoom, pan, and hover tooltips
- Large datasets (>100K rows) are automatically downsampled for performance
- The tool can read data from the same PostgreSQL database used by the SQL Query tool
