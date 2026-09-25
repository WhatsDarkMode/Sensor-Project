## ADR-005:
Use a hosted free-tier database (Supabase) instead of self-hosting an always-on server

## Context:
Sensor readings need somewhere to be written continuously, which implies
something needs to be listening and available whenever a reading arrives.

## Decision:
Use Supabase's hosted, free-tier Postgres database, with sensor nodes
posting directly to its REST API, rather than running a self-hosted
database/ingestion service on local hardware.

## Reasoning / Alternatives considered:
Considered running a local MQTT broker plus a self-hosted Postgres
instance (the original planned architecture) on a Raspberry Pi kept
running 24/7. Rejected as the default because it requires a piece of
infrastructure to be reliably available at all times, with associated
maintenance/uptime responsibility, for a personal project with limited
available time. A hosted free-tier database removes that entire
operational burden.

## Consequences:
No local infrastructure to maintain or keep powered on; sensor nodes can
be simple, and the project has no ongoing hosting cost. With no self-hosted 
server in the picture at all, there was no natural place for a separate backend 
to live even if one had been built.