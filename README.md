# HarnessEngineering

A Python library and command-line tool for designing and managing **wire harness assemblies** used in automotive, aerospace, and industrial engineering.

## Features

- **Data models** for harnesses, wires, and connectors with validation
- **CRUD operations** via `HarnessManager` with JSON file persistence
- **CLI tool** (`harness`) for interactive harness management

## Installation

```bash
pip install -e .
```

## Quick Start

```bash
# Create a harness
harness create "Engine Harness" --description "Main engine wiring loom"

# List harnesses
harness list

# Add a connector (use the ID printed by 'create')
harness add-connector <harness-id> "ECU Connector" --type "Deutsch DT" --pins 8

# Add a wire
harness add-wire <harness-id> "12V Power" \
    --gauge "18 AWG" --color "Red" --length 1200 \
    --from-connector "Battery" --from-pin 1 \
    --to-connector "ECU Connector" --to-pin 3

# Inspect full harness JSON
harness show <harness-id>

# Delete a harness
harness delete <harness-id>
```

By default, data is stored in `harnesses.json` in the current directory.
Use `--storage <path>` to specify a custom location.

## Python API

```python
from harness_engineering import Harness, Connector, ConnectorType, Wire, WireGauge, HarnessManager

manager = HarnessManager(storage_path="my_harnesses.json")

# Create a harness
harness = Harness(name="Engine Harness", description="Main engine loom")
connector = Connector(name="ECU", connector_type=ConnectorType.DEUTSCH_DT, pin_count=8)
wire = Wire(
    name="12V Power",
    gauge=WireGauge.AWG_18,
    color="Red",
    length_mm=1200.0,
    from_connector="Battery",
    from_pin=1,
    to_connector="ECU",
    to_pin=3,
)
harness.add_connector(connector)
harness.add_wire(wire)
manager.create(harness)

print(f"Total wire length: {harness.total_wire_length_mm()} mm")
```

## Development

```bash
pip install -e ".[dev]"
pytest
```
