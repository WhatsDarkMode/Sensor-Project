# Room Temperature & Weather Comparison

A small IoT + software project comparing indoor temperature and pressure
against outdoor weather, using an ESP32 sensor node and a hosted database.

## Live App
🔗 [Live App](https://sensor-project.streamlit.app/) — publicly viewable, no login required.

## Status
Complete (v1) — one working sensor node reporting to a public dashboard,
end to end. See "Future Improvements" below for what's deliberately out
of scope for this version.

## Known Limitations
- The sensor on node 1 was identified as a mislabeled BMP280 rather than
  a genuine BME280 (see `build-journey.md`) — it has no humidity sensor,
  so the dashboard currently compares temperature and pressure only.
- Only one sensor node has been built. The architecture supports multiple
  rooms (see `sensor-project-summary.md`), but that expansion wasn't
  completed for this version.

## Future Improvements
- Replace node 1's sensor with a genuine BME280 to restore humidity
- Build nodes 2 and 3 for additional rooms
- Add pytest coverage and CI

## Architecture
See `sensor-project-summary.md` for the full architecture, hardware plan,
and rationale.

## Decisions
See `decisions/` for documenting key design choices and trade-offs
made along the way.

## Build Journey
The steps were planned with Claude (AI), see `sensor-node-1-build-guide.md`. 
I thought it'd be useful to record the steps i actually took along the way too, 
these are recorded in `build-journey.md` 

## Photos
See `node/photos/` for photos of the physical build.

## Setup

### Hardware (per node)
| Item | Qty | Search Term | Approx cost |
| --- | --- | --- | --- |
| ESP32 dev board (pre-soldered headers) | 1 | ESP32 dev board with headers  | £11 |
| BME280 sensor breakout (pre-soldered)  | 1 | BME280 breakout pre-soldered  | £6  |
| Female-to-female jumper wires (pack)   | 1 | female to female jumper wires | £4  | 

### Node Configuration
Create `node/config.py` (not committed — see `.gitignore`):
```python
WIFI_SSID = "your-network-name"
WIFI_PASSWORD = "your-password"
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-publishable-key"
SUPABASE_NODE_EMAIL = "your-sensor-account-email"
SUPABASE_NODE_PW = "your-sensor-account-password"
```

### App Configuration
Create `app/.streamlit/secrets.toml` (not committed — see `.gitignore`):
```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-publishable-key"
HOME_LATITUDE = 53.4437
HOME_LONGITUDE = -2.3572
```

## Third-Party Code
`node/bme280_float.py` is a MicroPython BME280 driver by robert-hh
(https://github.com/robert-hh/BME280), included unmodified so the
project runs standalone.