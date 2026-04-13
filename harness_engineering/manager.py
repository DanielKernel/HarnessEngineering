"""HarnessManager: CRUD operations for harness assemblies with JSON persistence."""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional

from .models import Harness


class HarnessManager:
    """Manages a collection of harness assemblies with optional file-based persistence."""

    def __init__(self, storage_path: Optional[str] = None) -> None:
        self._harnesses: Dict[str, Harness] = {}
        self._storage_path = storage_path
        if storage_path and os.path.isfile(storage_path):
            self._load()

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def create(self, harness: Harness) -> Harness:
        """Add a new harness to the collection.

        Raises:
            ValueError: If a harness with the same ID already exists.
        """
        if harness.id in self._harnesses:
            raise ValueError(f"Harness with id '{harness.id}' already exists")
        self._harnesses[harness.id] = harness
        self._save()
        return harness

    def get(self, harness_id: str) -> Optional[Harness]:
        """Return the harness with the given ID, or None if not found."""
        return self._harnesses.get(harness_id)

    def list(self) -> List[Harness]:
        """Return all harnesses in the collection."""
        return list(self._harnesses.values())

    def update(self, harness: Harness) -> Harness:
        """Replace an existing harness.

        Raises:
            KeyError: If no harness with the given ID exists.
        """
        if harness.id not in self._harnesses:
            raise KeyError(f"Harness with id '{harness.id}' not found")
        self._harnesses[harness.id] = harness
        self._save()
        return harness

    def delete(self, harness_id: str) -> bool:
        """Remove a harness by ID.

        Returns:
            True if the harness was found and removed, False otherwise.
        """
        if harness_id not in self._harnesses:
            return False
        del self._harnesses[harness_id]
        self._save()
        return True

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def _save(self) -> None:
        if not self._storage_path:
            return
        data = {hid: h.to_dict() for hid, h in self._harnesses.items()}
        with open(self._storage_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)

    def _load(self) -> None:
        with open(self._storage_path, "r", encoding="utf-8") as fh:
            content = fh.read().strip()
        if not content:
            return
        data = json.loads(content)
        self._harnesses = {hid: Harness.from_dict(hdata) for hid, hdata in data.items()}

    def save_to_file(self, path: str) -> None:
        """Save all harnesses to the specified file path."""
        data = {hid: h.to_dict() for hid, h in self._harnesses.items()}
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)

    def load_from_file(self, path: str) -> None:
        """Load harnesses from the specified file path (merges into current collection)."""
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        for hid, hdata in data.items():
            self._harnesses[hid] = Harness.from_dict(hdata)
