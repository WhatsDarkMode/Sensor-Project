# Room Temperature & Weather Comparison

A small IoT + software project comparing indoor temperature across rooms
against outdoor weather, using ESP32 sensor nodes and a hosted database.

## Status
In progress — node 1 build underway.

## Architecture
See `sensor-project-summary.md` for the full architecture, hardware plan,
and rationale.

## Decisions
See `decisions/` for ADRs documenting key design choices along the way.

## Setup
See `sensor-node-1-build-guide.md` for the step-by-step build instructions.

You'll need a `config.py` file (not committed — see `.gitignore`) containing:

​```python
WIFI_SSID = "your-network-name"
WIFI_PASSWORD = "your-password"
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-api-key"
​```