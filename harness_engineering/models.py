"""Data models for the Harness Engineering system."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class WireGauge(str, Enum):
    """Standard AWG wire gauge sizes."""

    AWG_8 = "8 AWG"
    AWG_10 = "10 AWG"
    AWG_12 = "12 AWG"
    AWG_14 = "14 AWG"
    AWG_16 = "16 AWG"
    AWG_18 = "18 AWG"
    AWG_20 = "20 AWG"
    AWG_22 = "22 AWG"
    AWG_24 = "24 AWG"


class ConnectorType(str, Enum):
    """Common connector types used in harness engineering."""

    DEUTSCH_DT = "Deutsch DT"
    DEUTSCH_DTP = "Deutsch DTP"
    AMPSEAL = "AmpSeal"
    WEATHER_PACK = "WeatherPack"
    METRI_PACK = "MetriPack"
    CIRCULAR = "Circular"
    BLADE = "Blade"
    RING = "Ring"


@dataclass
class Connector:
    """Represents an electrical connector in a wire harness."""

    name: str
    connector_type: ConnectorType
    pin_count: int
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if self.pin_count <= 0:
            raise ValueError("pin_count must be a positive integer")
        if not self.name.strip():
            raise ValueError("name must not be empty")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "connector_type": self.connector_type.value,
            "pin_count": self.pin_count,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Connector":
        obj = cls(
            name=data["name"],
            connector_type=ConnectorType(data["connector_type"]),
            pin_count=data["pin_count"],
            description=data.get("description", ""),
        )
        obj.id = data.get("id", obj.id)
        return obj


@dataclass
class Wire:
    """Represents a single wire in a harness."""

    name: str
    gauge: WireGauge
    color: str
    length_mm: float
    from_connector: str
    from_pin: int
    to_connector: str
    to_pin: int
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if self.length_mm <= 0:
            raise ValueError("length_mm must be positive")
        if not self.name.strip():
            raise ValueError("name must not be empty")
        if not self.color.strip():
            raise ValueError("color must not be empty")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "gauge": self.gauge.value,
            "color": self.color,
            "length_mm": self.length_mm,
            "from_connector": self.from_connector,
            "from_pin": self.from_pin,
            "to_connector": self.to_connector,
            "to_pin": self.to_pin,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Wire":
        obj = cls(
            name=data["name"],
            gauge=WireGauge(data["gauge"]),
            color=data["color"],
            length_mm=data["length_mm"],
            from_connector=data["from_connector"],
            from_pin=data["from_pin"],
            to_connector=data["to_connector"],
            to_pin=data["to_pin"],
            description=data.get("description", ""),
        )
        obj.id = data.get("id", obj.id)
        return obj


@dataclass
class Harness:
    """Represents a complete wire harness assembly."""

    name: str
    description: str = ""
    connectors: List[Connector] = field(default_factory=list)
    wires: List[Wire] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name must not be empty")

    def add_connector(self, connector: Connector) -> None:
        """Add a connector to the harness."""
        if any(c.id == connector.id for c in self.connectors):
            raise ValueError(f"Connector '{connector.id}' already exists in this harness")
        self.connectors.append(connector)

    def remove_connector(self, connector_id: str) -> Optional[Connector]:
        """Remove a connector by ID and return it, or None if not found."""
        for i, c in enumerate(self.connectors):
            if c.id == connector_id:
                return self.connectors.pop(i)
        return None

    def get_connector(self, connector_id: str) -> Optional[Connector]:
        """Return a connector by ID, or None if not found."""
        return next((c for c in self.connectors if c.id == connector_id), None)

    def add_wire(self, wire: Wire) -> None:
        """Add a wire to the harness."""
        if any(w.id == wire.id for w in self.wires):
            raise ValueError(f"Wire '{wire.id}' already exists in this harness")
        self.wires.append(wire)

    def remove_wire(self, wire_id: str) -> Optional[Wire]:
        """Remove a wire by ID and return it, or None if not found."""
        for i, w in enumerate(self.wires):
            if w.id == wire_id:
                return self.wires.pop(i)
        return None

    def get_wire(self, wire_id: str) -> Optional[Wire]:
        """Return a wire by ID, or None if not found."""
        return next((w for w in self.wires if w.id == wire_id), None)

    def total_wire_length_mm(self) -> float:
        """Calculate the total wire length in millimeters."""
        return sum(w.length_mm for w in self.wires)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "connectors": [c.to_dict() for c in self.connectors],
            "wires": [w.to_dict() for w in self.wires],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Harness":
        obj = cls(
            name=data["name"],
            description=data.get("description", ""),
            connectors=[Connector.from_dict(c) for c in data.get("connectors", [])],
            wires=[Wire.from_dict(w) for w in data.get("wires", [])],
        )
        obj.id = data.get("id", obj.id)
        return obj
