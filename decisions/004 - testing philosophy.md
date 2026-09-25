## ADR-004:
Test database connectivity with a hardcoded value before wiring in real sensor data

## Context:
The full node pipeline has two independent pieces that could fail — the
sensor read (I2C, wiring, driver) and the WiFi/database connection
(network, authentication, RLS policy). Testing them together for the
first time risks not knowing which one actually broke if something goes
wrong.

## Decision:
Before connecting real sensor readings to the database POST request,
first sent a single hardcoded test value end-to-end (WiFi → Supabase
Auth login → insert), and confirmed it appeared correctly in the
`readings` table.

## Reasoning / Alternatives considered:
Could have built the full pipeline in one pass and debugged whatever
broke. Rejected this because a failure at that point would leave two
equally plausible causes (bad sensor read vs. bad network/database code)
to investigate simultaneously, with no way to narrow it down quickly.
Testing with a hardcoded value isolates the network/database path
completely, so a failure there is unambiguous.

## Consequences:
Adds one small extra step before full integration, but removes an entire
class of debugging ambiguity later — a worthwhile trade-off given limited
available time per session.