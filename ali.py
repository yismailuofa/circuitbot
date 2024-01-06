res = """To create a circuit that blinks an LED every 20 seconds using an Arduino Uno, I'll provide you with the bill of materials, pinouts, schematic, code, and any special instructions. Let's get started.

### Bill of Materials:
```json
[
    {"part":"Arduino Uno", "name":"uno", "value":"", "notes":"Arduino Uno microcontroller"},
    {"part":"LED", "name":"D1", "value":"red", "notes":"Blinking LED. Standard voltage range (2-3.3V)."},
    {"part":"Resistor", "name":"R1", "value":"220 ohm", "notes":"Current limiting resistor for LED at 5V"}
]
```

### Pinouts:
```json
{
    "Arduino Uno": ["5V", "3.3V", "GND", "AREF", "D0/RX", "D1/TX", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "A0", "A1", "A2", "A3", "A4/SDA", "A5/SCL"],
    "D1": ["anode", "cathode"],
    "R1": ["1", "2"]
}
```

### Schematic (List of Connections):
```json
[
    [{"name":"D1", "pin":"cathode"}, {"name": "uno", "pin":"GND"}], 
    [{"name":"D1", "pin":"anode"}, {"name": "R1", "pin":"2"}], 
    [{"name":"R1", "pin":"1"}, {"name": "uno", "pin":"D5"}]
]
```

### Arduino Uno Code:
```cpp
// LED Blink Every 20 Seconds
// This code controls an LED to blink every 20 seconds.

#define PIN_LED 5 // LED connected to Digital I/O 5

void setup() {
    pinMode(PIN_LED, OUTPUT); // Initialize LED pin as output
}

void loop() {
    digitalWrite(PIN_LED, HIGH); // Turn LED ON
    delay(20000); // Wait for 20 seconds (20000 milliseconds)
    digitalWrite(PIN_LED, LOW); // Turn LED OFF
    delay(20000); // Wait for another 20 seconds
}
```

### Instructions:
- This code uses only standard Arduino libraries. No additional libraries are needed.
- Assemble the circuit as per the schematic.
- Upload the provided code to the Arduino Uno using the Arduino IDE.
- Ensure that the LED and resistor are correctly oriented and connected.

This setup will make the LED blink on and off every 20 seconds. Remember to double-check connections and orientations of components when assembling the circuit."""

import re
import json
import subprocess


mappings = []


def parseRes(res):
    pattern = r"```json\s*(.*?)```"
    ans = re.findall(pattern, res, re.DOTALL)
    # print(ans)
    schematic = bom = arduinoCode = None
    for i, a in enumerate(ans):
        print(f"{i} NEW BLOCK\n {a}")
        a = json.loads(a)
        # check if is instance of a list of lists
        if (
            isinstance(a, list) and a[0] and isinstance(a[0], list)
        ):  # it is the schematic
            schematic = a
        elif isinstance(a, list) and a[0] and isinstance(a[0], dict):
            bom = a

    pattern = r"```cpp\s*(.*?)```"
    ans = re.findall(pattern, res, re.DOTALL)
    arduinoCode = ans[0]

    return schematic, bom, arduinoCode


def sendCodeToArduino(code):
    arduino_port = "/dev/ttyACM0"  # Replace with your Arduino's port
    sketch_path = "/path/to/your/sketch"  # Path to your Arduino sketch

    with open(sketch_path, "w") as f:
        f.write(code)

    compile_command = [
        "arduino-cli",
        "compile",
        "--fqbn",
        "arduino:avr:uno",
        sketch_path,
    ]
    upload_command = [
        "arduino-cli",
        "upload",
        "-p",
        arduino_port,
        "--fqbn",
        "arduino:avr:uno",
        sketch_path,
    ]

    # Compile the sketch
    subprocess.run(compile_command)

    # Upload the sketch
    subprocess.run(upload_command)


if __name__ == "__main__":
    schematic, bom, arduinoCode = parseRes(res)
    sendCodeToArduino(arduinoCode)
