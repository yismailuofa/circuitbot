res = """To create a circuit that blinks an LED every 20 seconds using an Arduino Uno, I'll provide you with the bill of materials, pinouts, schematic, code, and any special instructions. Let's get started.
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
from controller import Controller
from prompt import prompt
from openai import OpenAI


from component import Component


def parseRes(res):
    pattern = r"```json\s*(.*?)```"
    ans = re.findall(pattern, res, re.DOTALL)
    schematic = arduinoCode = None
    for a in ans:
        a = json.loads(a)
        # check if is instance of a list of lists
        if (
            isinstance(a, list) and a[0] and isinstance(a[0], list)
        ):  # it is the schematic
            schematic = a

    pattern = r"```cpp\s*(.*?)```"
    ans = re.findall(pattern, res, re.DOTALL)
    arduinoCode = ans[0]

    return schematic, arduinoCode


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


def createPrompt(task, components: list[Component]) -> str:
    if not task:
        task = (
            "Create a circuit that blinks an LED every 20 seconds using an Arduino Uno"
        )

    billOfMaterials = []
    pinouts = {}

    for c in components:
        billOfMaterials.append(
            {
                "part": c.partName,
                "name": c.name,
                "value": c.value,
            }
        )

        pinouts[c.partName] = list(c.pins.keys())

    formattedPrompt = prompt.format(
        task=task,
        billOfMaterials=json.dumps(billOfMaterials, indent=4),
        pinouts=json.dumps(pinouts, indent=4),
    )

    return formattedPrompt


def sendPrompt(prompt):
    client = OpenAI()
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    res = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            res += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")
    return res


if __name__ == "__main__":
    controller = Controller(
        components=[
            Component(
                name="R1",
                partName="Resistor",
                pins={"1": (0, 0), "2": (1, 0)},
                value="100 ohms",
            ),
            Component(
                name="R2",
                partName="Resistor",
                pins={"1": (0, 0), "2": (1, 0)},
                value="200 ohms",
            ),
            Component(
                name="R3",
                partName="Resistor",
                pins={"1": (0, 0), "2": (1, 0)},
                value="300 ohms",
            ),
            Component(
                name="D1",
                partName="LED",
                pins={"anode": (0, 0), "cathode": (1, 0)},
                value="Red",
            ),
            Component(
                name="uno",
                partName="Arduino Uno",
                pins={
                    "5V": (0, 0),
                    "3.3V": (0, 0),
                    "GND": (0, 0),
                    "AREF": (0, 0),
                    "D0/RX": (0, 0),
                    "D1/TX": (0, 0),
                    "D2": (0, 0),
                    "D3": (0, 0),
                    "D4": (0, 0),
                    "D5": (0, 0),
                    "D6": (0, 0),
                    "D7": (0, 0),
                    "D8": (0, 0),
                    "D9": (0, 0),
                    "D10": (0, 0),
                    "D11": (0, 0),
                    "D12": (0, 0),
                    "D13": (0, 0),
                    "A0": (0, 0),
                    "A1": (0, 0),
                    "A2": (0, 0),
                    "A3": (0, 0),
                    "A4/SDA": (0, 0),
                    "A5/SCL": (0, 0),
                },
            ),
        ]
    )

    formattedPrompt = createPrompt(
        input("Please describe a circuit to create: "), controller.components
    )

    # res = sendPrompt(formattedPrompt) UNCOMMENT TO HIT OPENAI
    schematic, arduinoCode = parseRes(res)

    if arduinoCode is None or schematic is None:
        print("Error: Could not parse response")
        exit(1)

    # sendCodeToArduino(arduinoCode) UNCOMMENT TO SEND CODE TO ARDUINO

    controller.executeSchematic(schematic)
