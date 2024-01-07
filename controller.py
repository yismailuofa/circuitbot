from dataclasses import dataclass, field

from component import Component
import serial


@dataclass
class Controller:
    port: str
    components: list[Component] = field(default_factory=list)

    def executeSchematic(self, schematic):
        # s = serial.Serial(self.port, 9600)
        # s.reset_input_buffer()
        s = serial.Serial()
        for cxn in schematic:
            self.executeConnection(cxn, s)

    def getComponentByName(self, name):
        for c in self.components:
            if c.name == name:
                return c

        return None

    def executeConnection(self, cxn, s):
        fr, to = cxn
        c1 = self.getComponentByName(fr["name"])
        c2 = self.getComponentByName(to["name"])

        if c1 is None or c2 is None:
            print("Error: Component not found")
            return

        print(
            f"Connecting {c1.name} pin {fr['pin']} ({c1.pins[fr['pin']]}) to {c2.name} pin {to['pin']} ({c2.pins[to['pin']]})"
        )
        self.connectPin(c1.pins[fr["pin"]], c2.pins[to["pin"]], s)

    def connectPin(self, fr, to, s):
        gCodes = self.createMoveCommands(fr, to)

        for gCode in gCodes:
            s.write(gCode)

    def createMoveCommands(self, fr, to):
        gCodes = []
        fr = convertTomm(fr)
        to = convertTomm(to)

        # Move to the first cxn
        gCodes.append(f"G0 X{fr[0]} Y{fr[1]} Z10")
        gCodes.append(f"G0 X{fr[0]} Y{fr[1]} Z0")

        # Grab the component
        gCodes.append("G1 GRAB")

        # Move to the second cxn
        gCodes.append(f"G0 X{fr[0]} Y{fr[1]} Z10")
        gCodes.append(f"G0 X{to[0]} Y{to[1]} Z10")

        gCodes.append(f"G0 X{to[0]} Y{to[1]} Z0")
        # Release the component

        gCodes.append("G1 REL")
        gCodes.append(f"G0 X{fr[0]} Y{fr[1]} Z10")

        return gCodes


def convertTomm(indexes):
    return (indexes[0] * 2.54, indexes[1] * 2.54)
