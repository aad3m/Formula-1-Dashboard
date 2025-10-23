APP_TITLE = "Formula 1 Live Dashboard"
APP_CAPTION = "Data: Jolpica (Ergast-compatible) • Charts: Plotly • App: Streamlit"

# Ergast-compatible Jolpica base
ERGAST_BASE = "https://api.jolpi.ca/ergast/f1"

# "current" or a specific year like "2025"

# Streamlit cache TTL (seconds)
CACHE_TTL = 300

# HTTP
HTTP_TIMEOUT = 20
HTTP_RETRIES = 3
HTTP_BACKOFF = 0.8  # base seconds; exponential backoff
USER_AGENT = "Formula-1-Dashboard/1.0"