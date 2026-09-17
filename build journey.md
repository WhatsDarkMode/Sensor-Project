## Build Steps taken
1. Connected the ESP32 board to the PC using provided USB-C cable
2. Confirmed the PC already had the correct USB-to-serial driver installed
   to communicate with the board.
    - To check this, I opened Device Manager and went to Ports. I was
      looking for a device name something like "CH340".
    - The board appeared there as "USB-SERIAL CH340", confirming the PC
      already had a working driver for it. So i didnt need to install a driver needed.
3. Downloaded and Installed Thonny, a free, beginner-friendly Python IDE
   with built-in support for flashing and programming MicroPython on
   boards like the ESP32.
4. Used Thonny to install MicroPython onto the board.
    - Opened Thonny
    - Bottom right, it initially showed "Local Python 3" (Thonny's default,
      for running plain Python on the PC itself) — clicked it and selected
      "Configure interpreter" to change this.
    - Set the interpreter to "MicroPython (ESP32)" and selected the correct
      COM port.
    - This opened the option to select Family, Variant, and Version for the
      firmware to flash. I selected the "Espressif ESP32 / WROOM" variant,
      as this is the generic, vendor-neutral build for the ESP32 chip
      itself, rather than one tailored to a specific manufacturer's board
      (e.g. SparkFun's own branded boards).
    - Clicked Install and waited a few minutes for the firmware to flash.
5. Confirmed MicroPython had installed successfully by running `help()` in
   the Shell, which returned the MicroPython welcome message and version
   info (v1.28.0, "Generic ESP32 module").
6. Wired the BME280 sensor to the board using female-to-female jumper wires.
    - I'm recording the wiring colour as i intend to use consistent wire     colours across each sensor node (if i add more), so that wiring stays easy to visually verify once there are multiple nodes to compare against each other.
    - BME280 pin -- ESP32 pin matchup (colour wire)
    - VCC -- 3.3V (red)
    - GND -- GND (black)
    - SCL -- GPIO22 (purple)
    - SDA -- GPIO21 (blue)
7. Verified the wiring using an I2C (I2C is a protocol) scanner in the Thonny Shell. Ran the following commands:
    - import machine
    - i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
    - print([hex(addr) for addr in i2c.scan()])
    - Result: ['0x76'] — confirms the BME280 is wired correctly and
      responding on the I2C bus at address 0x76.
8. Installed the BME280 MicroPython driver (bme280_float.py, by robert-hh - https://github.com/robert-hh/BME280) onto the ESP32 via Thonny. I also added created another script:
    - Wrote a short test script (node/main.py) that imports the driver,
      initialises it using the confirmed I2C address (0x76), and prints
      temperature, pressure, and humidity readings in a loop every 5
      seconds.
    - Ran the script and confirmed the values looked sane, roughly
      matching readings from my phone.
    - Saved and committed node/main.py to the repo.
9. Connected the ESP32 to home WiFi using MicroPython's built-in network
   module.
    - Created a 'config.py' file (excluded from git via '.gitignore') to
      store the WiFi SSID and password separately from the connection
      logic.
    - Wrote 'node/wifi_test.py', which builds a WLAN object in Station
      mode, activates the radio, and connects using the credentials imported from 'config.py'.
    - Ran the script and confirmed a successful connection:
      ('192.168.1.67', '255.255.255.0', '192.168.1.254', '192.168.1.254')
      — IP address, subnet mask, gateway, and DNS server, obtained
      automatically via DHCP.
10. Set up the hosted database (Supabase).
    - Created a free Supabase account and a new project.
    - Created a 'readings' table via the Table Editor: 'id' (auto
      primary key), 'room' (text), 'temperature' (float8), 'humidity'
      (float8), 'timestamp' (timestamptz, default 'now()').
    - Exposed the table via Integrations → Data API, confirming the
      'public' schema and 'readings' table were both enabled.
    - Created a dedicated Supabase Auth account to represent the sensor
      nodes, rather than relying on the publishable key alone — restricted the table's RLS insert policy to 'authenticated' users only, rather than the default "for all"
      template.
    - Retrieved the project URL and publishable API key from
      Settings → API Keys, and stored these — along with the sensor
      account's email/password — in 'config.py'.
    - Deliberately kept the project's secret API key and database
      password out of 'config.py' entirely, reserved for the future
      backend service only — the sensor node has no need for either.
11. Tested sending a reading to the hosted database, end to end, using a
    hardcoded test value.
    - Wrote 'node/api_test.py': connects to WiFi, authenticates against
      Supabase using the dedicated sensor account, then POSTs a
      hardcoded reading to the 'readings' table.
    - Ran the script and confirmed success: WiFi connected, auth
      returned 200, insert returned 201.
    - Verified directly in the Supabase Table Editor that the row was
      actually created.
12. Combined WiFi, sensor reading, and database logic into the final
    node script.
    - Split the logic into separate, reusable files rather than one
      large script: 'node/wifi.py' (connect(), with a timeout-based
      retry rather than an indefinite wait), 'node/db.py' (login() and
      insert_reading()), and 'node/main.py' (orchestrates the actual
      loop: connect, read sensor, insert, sleep 60s, repeat).
    - main.py logs in to Supabase once at startup (rather than on every
      loop cycle) and re-checks/reconnects WiFi each cycle, giving basic
      resilience against a dropped connection without needing a
      separate special-case reconnect block.
    - Wrapped the database insert in error handling so a single failed
      request logs the issue and lets the loop continue to the next
      cycle, rather than crashing the script outright.
    - Moved the earlier standalone 'wifi_test.py' and 'api_test.py'
      into 'node/dev_tests/'.
    - Confirmed 'main.py' is saved directly onto the device's root
      filesystem under this exact filename, since MicroPython
      automatically runs a file named 'main.py' on every power-on/reset.