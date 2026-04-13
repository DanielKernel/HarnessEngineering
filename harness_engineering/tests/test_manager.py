"""Unit tests for HarnessManager."""

import os
import tempfile

import pytest

from harness_engineering.manager import HarnessManager
from harness_engineering.models import (
    Connector,
    ConnectorType,
    Harness,
    Wire,
    WireGauge,
)


def _make_harness(name: str = "H1") -> Harness:
    return Harness(name=name, description=f"Test harness {name}")


class TestHarnessManager:
    def test_create_and_get(self):
        manager = HarnessManager()
        h = _make_harness()
        manager.create(h)
        assert manager.get(h.id) is h

    def test_create_duplicate(self):
        manager = HarnessManager()
        h = _make_harness()
        manager.create(h)
        with pytest.raises(ValueError):
            manager.create(h)

    def test_list_empty(self):
        manager = HarnessManager()
        assert manager.list() == []

    def test_list_multiple(self):
        manager = HarnessManager()
        h1 = _make_harness("H1")
        h2 = _make_harness("H2")
        manager.create(h1)
        manager.create(h2)
        result = manager.list()
        assert len(result) == 2

    def test_get_nonexistent(self):
        manager = HarnessManager()
        assert manager.get("no-such-id") is None

    def test_update(self):
        manager = HarnessManager()
        h = _make_harness()
        manager.create(h)
        h.description = "Updated"
        manager.update(h)
        assert manager.get(h.id).description == "Updated"

    def test_update_nonexistent(self):
        manager = HarnessManager()
        h = _make_harness()
        with pytest.raises(KeyError):
            manager.update(h)

    def test_delete(self):
        manager = HarnessManager()
        h = _make_harness()
        manager.create(h)
        assert manager.delete(h.id) is True
        assert manager.get(h.id) is None

    def test_delete_nonexistent(self):
        manager = HarnessManager()
        assert manager.delete("no-such-id") is False

    def test_persistence(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            path = tmp.name
        try:
            # Create and save
            manager = HarnessManager(storage_path=path)
            h = _make_harness()
            c = Connector(name="C1", connector_type=ConnectorType.DEUTSCH_DT, pin_count=4)
            w = Wire(
                name="W1", gauge=WireGauge.AWG_18, color="Red", length_mm=250.0,
                from_connector="C1", from_pin=1, to_connector="C2", to_pin=2,
            )
            h.add_connector(c)
            h.add_wire(w)
            manager.create(h)

            # Reload and verify
            manager2 = HarnessManager(storage_path=path)
            restored = manager2.get(h.id)
            assert restored is not None
            assert restored.name == h.name
            assert len(restored.connectors) == 1
            assert len(restored.wires) == 1
            assert restored.connectors[0].name == "C1"
            assert restored.wires[0].color == "Red"
        finally:
            os.unlink(path)

    def test_save_and_load_file(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            path = tmp.name
        try:
            manager = HarnessManager()
            manager.create(_make_harness("H1"))
            manager.create(_make_harness("H2"))
            manager.save_to_file(path)

            manager2 = HarnessManager()
            manager2.load_from_file(path)
            assert len(manager2.list()) == 2
        finally:
            os.unlink(path)
