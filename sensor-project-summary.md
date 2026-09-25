# Multi-Room Temperature & Weather Comparison Project — Summary
The architecture below describes the full 3-room target design; v1 deliberately stops after proving the whole pipeline end-to-end on a single node, rather than continuing to nodes 2/3 immediately

## Goal
Have fun and learn a few things while building a small, hands-on IoT + software project that demonstrates systems-integration skills (APIs, databases, testing, containers, CI).
I wanted to keep it somewhat practical, so thought it would be cool to develop a
temperature sensor that i could use to compare external vs internal temperature.

## Final Architecture
```
[Sensor node: room 1]  --\
[Sensor node: room 2]  ---> WiFi --> HTTPS POST --> Hosted DB (Supabase, free tier)
[Sensor node: room 3]  --/                                  |
                                                            v
                                          Streamlit app (fetches readings,
                                          fetches weather, computes comparison,
                                          renders dashboard — all in one place)
                                                            ^
                                                            |
                                                  Weather API (Open-Meteo)
```
**v1 status**: node 1 only, fully working end-to-end. Nodes 2/3 not yet built.
- **Sensor nodes**: identical ESP32 boards + BME280 sensors, one per room.
- **Data path**: each node reads the sensor, connects to home WiFi, sends an HTTPS request directly to a hosted database's API — no always-on device required at home.
- **App**: a single Streamlit app (Python) that fetches readings from Supabase, fetches current weather from Open-Meteo, computes the indoor-vs-outdoor comparison, and renders the dashboard — all within one app, run on demand rather than as an always-on service.
- **Weather comparison**: pulled from Open-Meteo (free, no API key required).

## Deployment
Deployed via Streamlit Community Cloud (free tier), deploying directly from the public GitHub repo. Secrets handled via Streamlit's own secrets management (.streamlit/secrets.toml locally, pasted into Community Cloud's deployment settings — never committed). See build-journey.md for the full deployment process.

## Hardware Plan (Full 3-Node Target)
All room nodes use identical, solder-free ESP32 boards (decided in favour of
using Raspberry Pi, to keep cost down and simplify build — a Pi can be added
later as an optional upgrade for one node). See `README.md` for breakdown of
the hardware parts and costs, but in sum, one node cost £21. 

## Running Costs
- **Electricity:** negligible — roughly £3–5/year total for all three nodes running continuously (calculated at the UK price cap of ~26.11p/kWh).
- **Software/APIs:** £0 — Python, Postgres, pytest, GitHub Actions (free tier), Open-Meteo, and Supabase/Neon (free tier) all have no cost for this scale of project.
- Nodes stay plugged in permanently (mains power) — battery power was considered and rejected as unnecessary complexity given the low electricity cost.

## Software Stack
- **Sensor nodes:** MicroPython on ESP32, I2C read from BME280, HTTPS POST to hosted DB.
- **Database:** hosted free-tier Postgres (Supabase) — removes need for an always-on local server.
- **App:** Python (Streamlit), all comparison/fetch logic organised into
  testable functions within the `app/` folder — no separate backend service.
- **Testing:** pytest — planned, not yet implemented.
- **Weather data:** Open-Meteo API (no auth required).

## Decisions and Roadmap
The reasoning behind key design choices made during this build are documented as individual write-ups in `decisions/`. The actual sequence of steps taken, including the mistakes and fixes along the way, is in `build-journey.md`. Both are more detailed and more current than anything a summary here could stay in sync with, so this document sticks to describing the architecture as it stands rather than repeating either.

## Open Questions / Next Steps
- Replace node 1's sensor with a genuine BME280 (current one is a mislabeled BMP280 — no humidity sensor) and reintroduce humidity.
- Build nodes 2 and 3.
- Add pytest coverage and a GitHub Actions CI workflow.
