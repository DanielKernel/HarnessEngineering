"""Command-line interface for the Harness Engineering system."""

from __future__ import annotations

import argparse
import json
import sys

from .manager import HarnessManager
from .models import Connector, ConnectorType, Harness, Wire, WireGauge


DEFAULT_STORAGE = "harnesses.json"


def _get_manager(args: argparse.Namespace) -> HarnessManager:
    return HarnessManager(storage_path=getattr(args, "storage", DEFAULT_STORAGE))


# ---------------------------------------------------------------------------
# Sub-command handlers
# ---------------------------------------------------------------------------

def cmd_list(args: argparse.Namespace) -> None:
    manager = _get_manager(args)
    harnesses = manager.list()
    if not harnesses:
        print("No harnesses found.")
        return
    for h in harnesses:
        print(f"  [{h.id[:8]}] {h.name} — {len(h.connectors)} connector(s), {len(h.wires)} wire(s)")


def cmd_create(args: argparse.Namespace) -> None:
    manager = _get_manager(args)
    harness = Harness(name=args.name, description=args.description or "")
    manager.create(harness)
    print(f"Created harness '{harness.name}' (id: {harness.id})")


def cmd_show(args: argparse.Namespace) -> None:
    manager = _get_manager(args)
    harness = manager.get(args.id)
    if harness is None:
        print(f"Harness '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(harness.to_dict(), indent=2))


def cmd_delete(args: argparse.Namespace) -> None:
    manager = _get_manager(args)
    if manager.delete(args.id):
        print(f"Deleted harness '{args.id}'.")
    else:
        print(f"Harness '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)


def cmd_add_connector(args: argparse.Namespace) -> None:
    manager = _get_manager(args)
    harness = manager.get(args.harness_id)
    if harness is None:
        print(f"Harness '{args.harness_id}' not found.", file=sys.stderr)
        sys.exit(1)
    connector = Connector(
        name=args.name,
        connector_type=ConnectorType(args.type),
        pin_count=args.pins,
        description=args.description or "",
    )
    harness.add_connector(connector)
    manager.update(harness)
    print(f"Added connector '{connector.name}' (id: {connector.id}) to harness '{harness.name}'.")


def cmd_add_wire(args: argparse.Namespace) -> None:
    manager = _get_manager(args)
    harness = manager.get(args.harness_id)
    if harness is None:
        print(f"Harness '{args.harness_id}' not found.", file=sys.stderr)
        sys.exit(1)
    wire = Wire(
        name=args.name,
        gauge=WireGauge(args.gauge),
        color=args.color,
        length_mm=args.length,
        from_connector=args.from_connector,
        from_pin=args.from_pin,
        to_connector=args.to_connector,
        to_pin=args.to_pin,
        description=args.description or "",
    )
    harness.add_wire(wire)
    manager.update(harness)
    print(f"Added wire '{wire.name}' (id: {wire.id}) to harness '{harness.name}'.")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="harness",
        description="Harness Engineering — wire harness design and management tool",
    )
    parser.add_argument(
        "--storage",
        default=DEFAULT_STORAGE,
        metavar="FILE",
        help="JSON storage file path (default: harnesses.json)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # list
    sub.add_parser("list", help="List all harnesses")

    # create
    p_create = sub.add_parser("create", help="Create a new harness")
    p_create.add_argument("name", help="Harness name")
    p_create.add_argument("--description", "-d", help="Optional description")

    # show
    p_show = sub.add_parser("show", help="Show harness details as JSON")
    p_show.add_argument("id", help="Harness ID")

    # delete
    p_del = sub.add_parser("delete", help="Delete a harness")
    p_del.add_argument("id", help="Harness ID")

    # add-connector
    p_ac = sub.add_parser("add-connector", help="Add a connector to a harness")
    p_ac.add_argument("harness_id", help="Harness ID")
    p_ac.add_argument("name", help="Connector name")
    p_ac.add_argument(
        "--type",
        required=True,
        choices=[ct.value for ct in ConnectorType],
        help="Connector type",
    )
    p_ac.add_argument("--pins", type=int, required=True, help="Number of pins")
    p_ac.add_argument("--description", "-d", help="Optional description")

    # add-wire
    p_aw = sub.add_parser("add-wire", help="Add a wire to a harness")
    p_aw.add_argument("harness_id", help="Harness ID")
    p_aw.add_argument("name", help="Wire name")
    p_aw.add_argument(
        "--gauge",
        required=True,
        choices=[g.value for g in WireGauge],
        help="Wire gauge",
    )
    p_aw.add_argument("--color", required=True, help="Wire color")
    p_aw.add_argument("--length", type=float, required=True, help="Wire length in mm")
    p_aw.add_argument("--from-connector", required=True, dest="from_connector", help="Source connector name/id")
    p_aw.add_argument("--from-pin", type=int, required=True, dest="from_pin", help="Source pin number")
    p_aw.add_argument("--to-connector", required=True, dest="to_connector", help="Target connector name/id")
    p_aw.add_argument("--to-pin", type=int, required=True, dest="to_pin", help="Target pin number")
    p_aw.add_argument("--description", "-d", help="Optional description")

    return parser


_HANDLERS = {
    "list": cmd_list,
    "create": cmd_create,
    "show": cmd_show,
    "delete": cmd_delete,
    "add-connector": cmd_add_connector,
    "add-wire": cmd_add_wire,
}


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = _HANDLERS.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
