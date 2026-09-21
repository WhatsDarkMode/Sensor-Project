# ADR-002: Keep comparison logic inside the Streamlit app, rather than a separate API service

Date: 2026-09-21
Status: Accepted

## Context

The dashboard needs to do more than just display raw sensor readings — it
needs to fetch external weather data (from Open-Meteo) and compute a
comparison between indoor readings and outdoor conditions, per room. That
logic has to live somewhere, since Supabase's own auto-generated REST API
only ever serves raw rows from the `readings` table — it has no ability to
also fetch external weather data or perform any calculation on top.

An earlier version of the project plan assumed this logic would live in a
separate FastAPI backend service, with Streamlit calling that service
rather than doing any computation itself.

## Decision

Build the comparison logic directly inside the Streamlit app — fetching
from Supabase, fetching from Open-Meteo, and computing the comparison all
within the same script that renders the dashboard. No separate API service.

## Reasoning / Alternatives Considered

A separate FastAPI service was considered, and was the original plan.
Rejected here because the actual justification for that extra layer —
having a reusable service other consumers could call independently of the
dashboard — doesn't apply to this project. There is exactly one consumer
of this logic: the dashboard itself, used by me and a small number of
other people viewing it directly. Building a separate API purely for
architectural appearance, with no second real consumer to justify it,
would be adding complexity without a genuine corresponding benefit — the
kind of over-engineering that's arguably a worse signal than building the
right-sized solution for the actual problem.

The separate-API approach remains the right call if the project ever
grows a second real consumer of this logic (a second dashboard, a mobile
app, etc.) — at that point the justification would be genuine rather than
assumed in advance.

## Consequences

- Fewer moving parts to build, deploy, and maintain — one Streamlit app
  rather than two separate services.
- Comparison logic is coupled to the dashboard rather than independently
  reusable — an accepted limitation, since no second consumer currently
  exists.
- The originally planned `api` folder is no longer needed for this
  purpose; comparison logic will instead live within the Streamlit app's
  own code, organised into clear functions for testability even without a
  separate service boundary.