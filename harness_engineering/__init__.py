"""Harness Engineering - Wire harness design and management system."""

from .models import Connector, Wire, Harness
from .manager import HarnessManager

__all__ = ["Connector", "Wire", "Harness", "HarnessManager"]
__version__ = "0.1.0"
