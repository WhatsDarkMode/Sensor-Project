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