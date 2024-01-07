from dataclasses import dataclass, field

from component import Component


@dataclass
class Controller:
    components: list[Component] = field(default_factory=list)

    def executeSchematic(self, schematic):
        for cxn in schematic:
            self.executeConnection(cxn)

    def getComponentByName(self, name):
        for c in self.components:
            if c.name == name:
                return c

        return None

    def executeConnection(self, cxn):
        fr, to = cxn
        c1 = self.getComponentByName(fr["name"])
        c2 = self.getComponentByName(to["name"])

        if c1 is None or c2 is None:
            print("Error: Component not found")
            return

        print(
            f"Connecting {c1.name} pin {fr['pin']} ({c1.pins[fr['pin']]}) to {c2.name} pin {to['pin']} ({c2.pins[to['pin']]})"
        )
