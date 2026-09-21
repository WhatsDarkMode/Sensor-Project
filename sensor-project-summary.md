# Multi-Room Temperature & Weather Comparison Project — Summary

## Goal

Build a small, hands-on IoT + software project that demonstrates systems-integration
skills (APIs, databases, testing, containers, CI) for a CV/portfolio, while staying
genuinely engaging by solving a real personal question: **how does each room's
temperature compare to the outside weather over time?**

Chosen deliberately to sit between two options — a pure hardware tutorial (low
CV value) and a pure software integration project (less hands-on/engaging) —
by combining both: real sensors in real rooms, feeding a properly engineered
software stack.

## Final Architecture

```
[Sensor node: room 1]  --\
[Sensor node: room 2]  ---> WiFi --> HTTPS POST --> Hosted DB (Supabase, free tier)
[Sensor node: room 3]  --/                                |
                                                            v
                                          Streamlit app (fetches readings,
                                          fetches weather, computes comparison,
                                          renders dashboard — all in one place)
                                                            ^
                                                            |
                                                  Weather API (Open-Meteo)
```

- **Sensor nodes:** identical ESP32 boards + BME280 sensors, one per room.
- **Data path:** each node reads the sensor, connects to home WiFi, sends an
  HTTPS request directly to a hosted database's API — no always-on device
  required at home.
- **App:** a single Streamlit app (Python) that fetches readings from
  Supabase, fetches current weather from Open-Meteo, computes the
  indoor-vs-outdoor comparison, and renders the dashboard — all within one
  app, run on demand rather than as an always-on service (see
  `decisions/` for why a separate backend API was deliberately not built).
- **Weather comparison:** pulled from Open-Meteo (free, no API key required).

## Hardware Plan

All room nodes use identical, solder-free ESP32 boards (decided in favour of
using Raspberry Pi, to keep cost down and simplify build — a Pi can be added
later as an optional upgrade for one node).

| Item | Qty | Search term | Approx cost |
|---|---|---|---|
| ESP32 dev board (pre-soldered headers) | 3 | "ESP32 dev board with headers" | £5–8 each |
| BME280 sensor breakout (pre-soldered) | 3 | "BME280 breakout pre-soldered" | £4–6 each |
| Female-to-female jumper wires (pack) | 1 | "female to female jumper wires" | £3–5 |
| USB cable per board | 3 | check connector type in listing | £3–5 each |

**Total: ~£39–62, one-off, all three rooms.**

Buying notes:
- Check listing **photos**, not just titles, for "pre-soldered" — inconsistent labelling is common.
- Buy jumper wires once; reused across all three nodes.

## Running Costs

- **Electricity:** negligible — roughly £3–5/year total for all three nodes running continuously (calculated at the UK price cap of ~26.11p/kWh).
- **Software/APIs:** £0 — Python, Docker, Postgres, pytest, GitHub Actions (free tier), Open-Meteo, and Supabase/Neon (free tier) all have no cost for this scale of project.
- Nodes stay plugged in permanently (mains power) — battery power was considered and rejected as unnecessary complexity given the low electricity cost.

## Software Stack

- **Sensor nodes:** MicroPython on ESP32, I2C read from BME280, HTTPS POST to hosted DB.
- **Database:** hosted free-tier Postgres (Supabase) — removes need for an always-on local server.
- **App:** Python (Streamlit), all comparison/fetch logic organised into
  testable functions within the `app/` folder — no separate backend service.
- **Testing:** pytest, covering validation/comparison logic (not hardware itself).
- **CI:** GitHub Actions — runs tests on every push.
- **Weather data:** Open-Meteo API (no auth required).

## Build Roadmap (session-sized phases)

1. Get one sensor node reading values (hardware + MicroPython script)
2. Refactor into testable logic + pytest coverage
3. Send readings via HTTPS to hosted DB
4. Repeat for rooms 2 and 3
5. Build the Streamlit app: fetch readings, pull weather data, compute
   comparisons, render charts — all within `app/`
6. Add GitHub Actions CI (tests)
7. Deploy via Streamlit Community Cloud (free) so it's viewable via a
   shareable link, not just locally
9. Optional: alert/webhook (e.g. Slack) when a room deviates unexpectedly from outside temp
10. Optional future upgrade: swap one ESP32 node for a Raspberry Pi Zero 2 W, for the full-Linux/Docker-on-device experience

## Key Decisions & Rationale

| Decision | Reasoning |
|---|---|
| ESP32 over Raspberry Pi for all room nodes | Cheaper, simpler, sufficient for "read + send" job; Pi's full-OS capability isn't needed at the sensor |
| Hosted free-tier DB instead of self-hosted, always-on server | Removes uptime/electricity concerns, no server to maintain at home |
| HTTPS POST instead of MQTT (for now) | Simpler to implement first; MQTT can be added later as a "v2" if desired |
| Comparison logic inside the Streamlit app, not a separate API | Only one consumer of this logic exists (the dashboard) — a separate service would add complexity with no real corresponding benefit at this project's scale (see ADR) |
| Pre-soldered components only | Avoids soldering as a blocker to limited free time |
| CV framing: "config-driven integration" over "temperature sensor project" | Better reflects the actual engineering skills demonstrated |

## Open Questions / Next Steps

- Build `app/` — the Streamlit dashboard: fetch from Supabase, fetch from
  Open-Meteo, compute comparison, render charts.
- Node 1 currently sends temperature/pressure only (humidity sensor
  identified as a mislabeled BMP280 — see build log); replace with a
  genuine BME280 and reintroduce humidity once confirmed.
- Repeat node build for rooms 2 and 3.
