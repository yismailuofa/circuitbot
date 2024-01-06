from dataclasses import dataclass, field


@dataclass
class Component:
    name: str
    partName: str
    pins: dict = field(default_factory=dict)
    value: str = ""
    isPlaced: bool = False
