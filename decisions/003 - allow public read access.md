# ADR-003: Allow public read access to readings, while keeping writes restricted to authenticated sensor accounts

Date: 2026-09-21
Status: Accepted

## Context

The dashboard needs to read from the `readings` table. By default, RLS
denies all access until a policy explicitly grants it — at this point,
only an INSERT policy exists (restricted to authenticated sensor
accounts, per an earlier decision). No SELECT policy exists yet, so
nothing can currently read from the table at all, including the
dashboard.

The dashboard is intended to be viewable by other people, including
potential employers, without requiring them to have an account or share a
login.

## Decision

Add a new RLS policy allowing SELECT (read) access to everyone, with no
authentication required. Writing (INSERT) remains restricted to
authenticated sensor accounts only, unchanged from the earlier decision.

## Reasoning / Alternatives Considered

Considered requiring the dashboard to log in the same way the sensor
nodes do (a dedicated "viewer" account, same pattern as the sensor
account). Rejected because it would require distributing a login to
anyone wanting to view the dashboard, directly working against the goal
of it being easily viewable by other people without setup on their end.

The risk profile of reading versus writing is genuinely asymmetric here,
which is why the two operations warrant different policies rather than
matching restriction levels for consistency's own sake. Allowing public
writes would let anyone pollute the dataset with garbage data, degrading
the project's actual purpose. Allowing public reads only exposes
temperature and pressure readings — data with no real sensitivity — so
the actual cost of exposing it is low, while the benefit (frictionless
public viewing) is genuine and directly serves the project's goal.

## Consequences

- Anyone with the project URL and publishable key can read all sensor
  data — acceptable, given the data itself isn't sensitive.
- Writing remains properly restricted, so the integrity of the dataset
  is still protected from anonymous tampering.
- If the project ever stored genuinely sensitive data in the same table
  in future, this policy would need to be revisited rather than assumed
  to still be appropriate.