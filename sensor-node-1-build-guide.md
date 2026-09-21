# Sensor Node 1 — Step-by-Step Build Guide

Companion to `sensor-project-summary.md`. This is the actual build sequence
for getting the first room's ESP32 + BME280 fully working, end to end.

**Before you start:** create the GitHub repo now, even empty — add a
`README.md` and a `NOTES.md` (for troubleshooting log/hardware gremlins).
Commit as you complete each step below, not all at the end — that commit
history is itself useful documentation of the process.

**Important, do this once and don't skip it:** create a `config.py` file to
hold your WiFi password and database API key, and add it to `.gitignore`
immediately, before you write anything else. This stops you accidentally
committing real credentials to a public GitHub repo later — a genuinely
common, embarrassing mistake that's much easier to prevent than fix after
the fact.

---

## Step 1 — Set Up Your Development Environment

- Install **Thonny** (free, beginner-friendly Python IDE with built-in
  MicroPython/ESP32 support — no separate toolchain needed).
- Download the MicroPython firmware for ESP32 from micropython.org.
- Flash it onto the ESP32: in Thonny, go to Tools → Options →
  Interpreter → select "MicroPython (ESP32)" → install/flash the firmware
  file you downloaded. Connect the ESP32 via USB first.
- Confirm it worked: Thonny's shell should connect to the board and show a
  MicroPython prompt (`>>>`).

## Step 2 — Wire the BME280 to the ESP32 (Physical Assembly)

Four wires, direct female-to-female jumpers, no breadboard needed:

| BME280 pin | ESP32 pin |
|---|---|
| VCC | 3.3V (**not** 5V — check your specific breakout's voltage rating) |
| GND | GND |
| SCL | GPIO22 |
| SDA | GPIO21 |

GPIO21/22 are the standard default I2C pins on most ESP32 dev boards, but
double-check your specific board's pinout diagram/silkscreen labels before
wiring, since layouts vary slightly between manufacturers.

**Double-check every connection before powering on.**

## Step 3 — Verify the Wiring: I2C Scanner

Before writing any real logic, run a short I2C scanner script — a handful
of lines that just asks "what devices are visible on the I2C bus, and at
what address?" This isolates wiring problems from code problems early,
rather than debugging both at once later.

You're looking for the BME280 to show up at address `0x76` or `0x77`
(varies by breakout board). If nothing shows up, it's a wiring issue —
recheck connections before going further.

## Step 4 — Install a BME280 Driver and Read Real Values

- Copy a MicroPython BME280 driver file onto the device's filesystem (small,
  single-file, well-established community libraries exist for this — Thonny
  lets you upload a `.py` file directly onto the ESP32).
- Write a short script that initialises the sensor using that driver and
  prints temperature/humidity in a loop, every few seconds.
- Confirm the values look sane (compare against a phone weather app or
  another thermometer, roughly).

**Commit point:** you now have a working sensor read — commit this as its
own small step.

## Step 5 — Get WiFi Connecting

- Using MicroPython's built-in `network` module, write and test a short
  script that connects to your home WiFi (SSID + password, pulled from your
  gitignored `config.py`, not hardcoded).
- Confirm it successfully obtains an IP address before moving on.

## Step 6 — Set Up the Hosted Database (Supabase)

- Create a free Supabase account and a new project.
- Define a `readings` table: columns for `id`, `room`, `temperature`,
  `humidity`, and `timestamp`.
- From the project settings, grab the API URL and the public API key —
  store these in `config.py` too, not in the script itself.

## Step 7 — Send a Single Test Reading

- Using MicroPython's `urequests` library (a lightweight `requests`
  equivalent), write a script that POSTs a JSON payload to Supabase's REST
  endpoint for your `readings` table.
- Test this with a **hardcoded** value first (e.g. a fake temperature) —
  confirm it actually appears in the Supabase table before wiring in real
  sensor data. Isolating this step means if something fails, you know
  immediately whether it's the database connection or the sensor reading
  that's the problem.

## Step 8 — Combine Into the Full Node Script

Now bring Steps 4, 5, and 7 together into one script that:
1. Connects to WiFi
2. Reads the sensor
3. POSTs the reading to Supabase
4. Sleeps (e.g. 60 seconds)
5. Repeats

Add basic error handling — retry WiFi if it drops, retry the POST if it
fails — this is good practice generally, and also genuinely good material
to document in your README as a deliberate design decision.

## Step 9 — Let It Run

Leave the node running for a while (an hour, then overnight) and confirm
readings are arriving continuously in Supabase, with timestamps that make
sense and no unexplained gaps.

## Step 10 — Document and Commit Properly

- Write the README: what hardware is used, the wiring table from Step 2,
  how to flash the firmware, and how to set up your own `config.py` (with a
  `config.py.example` template showing the expected format, but no real
  credentials).
- Commit the script(s), README, and any notes on issues you hit along the
  way (pulled from your running `NOTES.md`).

---

Once node 1 is solid end-to-end, repeat Steps 1-2 (dev environment setup is
one-time, so really just Step 2 wiring + reflashing) for the other two
rooms — the script itself only needs the `room` value changed per node.
