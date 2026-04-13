"""Unit tests for Harness Engineering models."""

import pytest

from harness_engineering.models import (
    Connector,
    ConnectorType,
    Harness,
    Wire,
    WireGauge,
)


# ---------------------------------------------------------------------------
# Connector tests
# ---------------------------------------------------------------------------

class TestConnector:
    def test_create_valid(self):
        c = Connector(name="C1", connector_type=ConnectorType.DEUTSCH_DT, pin_count=4)
        assert c.name == "C1"
        assert c.pin_count == 4
        assert c.id  # UUID assigned

    def test_invalid_pin_count(self):
        with pytest.raises(ValueError):
            Connector(name="C1", connector_type=ConnectorType.DEUTSCH_DT, pin_count=0)

    def test_empty_name(self):
        with pytest.raises(ValueError):
            Connector(name="  ", connector_type=ConnectorType.DEUTSCH_DT, pin_count=2)

    def test_roundtrip(self):
        c = Connector(name="C1", connector_type=ConnectorType.AMPSEAL, pin_count=8, description="Test")
        restored = Connector.from_dict(c.to_dict())
        assert restored.id == c.id
        assert restored.name == c.name
        assert restored.connector_type == c.connector_type
        assert restored.pin_count == c.pin_count
        assert restored.description == c.description


# ---------------------------------------------------------------------------
# Wire tests
# ---------------------------------------------------------------------------

class TestWire:
    def _make_wire(self, **kwargs):
        defaults = dict(
            name="W1",
            gauge=WireGauge.AWG_18,
            color="Red",
            length_mm=500.0,
            from_connector="C1",
            from_pin=1,
            to_connector="C2",
            to_pin=1,
        )
        defaults.update(kwargs)
        return Wire(**defaults)

    def test_create_valid(self):
        w = self._make_wire()
        assert w.name == "W1"
        assert w.gauge == WireGauge.AWG_18
        assert w.length_mm == 500.0

    def test_invalid_length(self):
        with pytest.raises(ValueError):
            self._make_wire(length_mm=0)

    def test_empty_color(self):
        with pytest.raises(ValueError):
            self._make_wire(color="")

    def test_roundtrip(self):
        w = self._make_wire(description="main power")
        restored = Wire.from_dict(w.to_dict())
        assert restored.id == w.id
        assert restored.gauge == w.gauge
        assert restored.color == w.color
        assert restored.length_mm == w.length_mm
        assert restored.from_connector == w.from_connector
        assert restored.from_pin == w.from_pin


# ---------------------------------------------------------------------------
# Harness tests
# ---------------------------------------------------------------------------

class TestHarness:
    def _make_connector(self, name="C1"):
        return Connector(name=name, connector_type=ConnectorType.DEUTSCH_DT, pin_count=4)

    def _make_wire(self, name="W1"):
        return Wire(
            name=name,
            gauge=WireGauge.AWG_20,
            color="Blue",
            length_mm=300.0,
            from_connector="C1",
            from_pin=1,
            to_connector="C2",
            to_pin=2,
        )

    def test_create_valid(self):
        h = Harness(name="H1", description="Test harness")
        assert h.name == "H1"
        assert h.connectors == []
        assert h.wires == []

    def test_empty_name(self):
        with pytest.raises(ValueError):
            Harness(name="")

    def test_add_connector(self):
        h = Harness(name="H1")
        c = self._make_connector()
        h.add_connector(c)
        assert len(h.connectors) == 1
        assert h.get_connector(c.id) is c

    def test_add_duplicate_connector(self):
        h = Harness(name="H1")
        c = self._make_connector()
        h.add_connector(c)
        with pytest.raises(ValueError):
            h.add_connector(c)

    def test_remove_connector(self):
        h = Harness(name="H1")
        c = self._make_connector()
        h.add_connector(c)
        removed = h.remove_connector(c.id)
        assert removed is c
        assert len(h.connectors) == 0

    def test_remove_nonexistent_connector(self):
        h = Harness(name="H1")
        result = h.remove_connector("nonexistent")
        assert result is None

    def test_add_wire(self):
        h = Harness(name="H1")
        w = self._make_wire()
        h.add_wire(w)
        assert len(h.wires) == 1
        assert h.get_wire(w.id) is w

    def test_add_duplicate_wire(self):
        h = Harness(name="H1")
        w = self._make_wire()
        h.add_wire(w)
        with pytest.raises(ValueError):
            h.add_wire(w)

    def test_remove_wire(self):
        h = Harness(name="H1")
        w = self._make_wire()
        h.add_wire(w)
        removed = h.remove_wire(w.id)
        assert removed is w
        assert len(h.wires) == 0

    def test_total_wire_length(self):
        h = Harness(name="H1")
        h.add_wire(self._make_wire("W1"))
        w2 = Wire(
            name="W2", gauge=WireGauge.AWG_20, color="Green", length_mm=700.0,
            from_connector="C1", from_pin=2, to_connector="C2", to_pin=3,
        )
        h.add_wire(w2)
        assert h.total_wire_length_mm() == pytest.approx(1000.0)

    def test_roundtrip(self):
        h = Harness(name="H1", description="desc")
        h.add_connector(self._make_connector())
        h.add_wire(self._make_wire())
        restored = Harness.from_dict(h.to_dict())
        assert restored.id == h.id
        assert restored.name == h.name
        assert len(restored.connectors) == 1
        assert len(restored.wires) == 1
