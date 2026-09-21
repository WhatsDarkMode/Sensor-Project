## ADR-001: 
Use ESP32 boards instead of Raspberry Pi for all room sensor nodes

## Context: 
Each room needs a device to read a sensor and transmit the value; the original plan used a Raspberry Pi Zero 2 W for this role.

## Decision: 
Use ESP32 microcontrollers for all room nodes instead.

## Reasoning / Alternatives considered: 
A Pi Zero 2 W was originally chosen on the assumption it would also run Docker/the backend services locally. Once the architecture moved to a hosted database (see ADR-003), no room node needs to run anything beyond "read a sensor, send an HTTP request" — a job a much simpler, cheaper microcontroller handles fine. An ESP32 is roughly a third of the cost, requires no OS/SD card management, and is sufficient for this specific, narrow task. The tradeoff is MicroPython instead of full Python, and no ability to run Docker on the node itself — both acceptable given the node's job is intentionally minimal.

## Consequences: 
Meaningfully lower hardware cost across three rooms; identical code/hardware across all nodes, simplifying the build. Leaves the option open to swap a single node for a Raspberry Pi later specifically to gain full-Linux/Docker experience on that one device, as a deliberate future upgrade rather than a default.