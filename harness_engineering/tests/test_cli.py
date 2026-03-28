"""Unit tests for the CLI interface."""

import json
import os
import tempfile

import pytest

from harness_engineering.cli import main


@pytest.fixture
def storage():
    """Provide a temporary JSON storage file, deleted after each test."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        path = tmp.name
    yield path
    if os.path.exists(path):
        os.unlink(path)


def run(*args, storage_path: str) -> None:
    """Helper to invoke the CLI with the shared storage file."""
    main(["--storage", storage_path, *args])


class TestCLI:
    def test_list_empty(self, storage, capsys):
        run("list", storage_path=storage)
        out = capsys.readouterr().out
        assert "No harnesses found" in out

    def test_create_and_list(self, storage, capsys):
        run("create", "MyHarness", "--description", "A test", storage_path=storage)
        capsys.readouterr()  # clear

        run("list", storage_path=storage)
        out = capsys.readouterr().out
        assert "MyHarness" in out

    def test_show(self, storage, capsys):
        run("create", "MyHarness", storage_path=storage)
        out = capsys.readouterr().out
        harness_id = out.split("id: ")[1].strip().rstrip(")")

        run("show", harness_id, storage_path=storage)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["name"] == "MyHarness"
        assert data["id"] == harness_id

    def test_delete(self, storage, capsys):
        run("create", "ToDelete", storage_path=storage)
        out = capsys.readouterr().out
        harness_id = out.split("id: ")[1].strip().rstrip(")")

        run("delete", harness_id, storage_path=storage)
        out = capsys.readouterr().out
        assert "Deleted" in out

        run("list", storage_path=storage)
        out = capsys.readouterr().out
        assert "No harnesses found" in out

    def test_add_connector(self, storage, capsys):
        run("create", "H1", storage_path=storage)
        out = capsys.readouterr().out
        harness_id = out.split("id: ")[1].strip().rstrip(")")

        run(
            "add-connector", harness_id, "C1",
            "--type", "Deutsch DT",
            "--pins", "4",
            storage_path=storage,
        )
        out = capsys.readouterr().out
        assert "C1" in out

        run("show", harness_id, storage_path=storage)
        data = json.loads(capsys.readouterr().out)
        assert len(data["connectors"]) == 1
        assert data["connectors"][0]["name"] == "C1"

    def test_add_wire(self, storage, capsys):
        run("create", "H1", storage_path=storage)
        out = capsys.readouterr().out
        harness_id = out.split("id: ")[1].strip().rstrip(")")

        run(
            "add-wire", harness_id, "W1",
            "--gauge", "18 AWG",
            "--color", "Red",
            "--length", "500",
            "--from-connector", "C1",
            "--from-pin", "1",
            "--to-connector", "C2",
            "--to-pin", "2",
            storage_path=storage,
        )
        out = capsys.readouterr().out
        assert "W1" in out

        run("show", harness_id, storage_path=storage)
        data = json.loads(capsys.readouterr().out)
        assert len(data["wires"]) == 1
        assert data["wires"][0]["color"] == "Red"

    def test_show_nonexistent(self, storage):
        with pytest.raises(SystemExit) as exc:
            run("show", "no-such-id", storage_path=storage)
        assert exc.value.code == 1

    def test_delete_nonexistent(self, storage):
        with pytest.raises(SystemExit) as exc:
            run("delete", "no-such-id", storage_path=storage)
        assert exc.value.code == 1
