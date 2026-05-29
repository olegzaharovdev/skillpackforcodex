#!/usr/bin/env python3
"""Validate sidechat protocol machine exports.

Checks:
- manifest.json is valid JSON when present
- normalized.json is valid JSON and has required fields
- timeline.jsonl has one valid JSON object per non-empty line
- every timeline event has a type field
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys


REQUIRED_NORMALIZED_FIELDS = {
    "schema",
    "protocol_id",
    "topic",
    "project",
    "workspace",
    "human_protocol_folder",
    "machine_export_folder",
    "limitations",
}


def load_json(path: pathlib.Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Invalid JSON: {path}: {exc}") from exc


def validate_normalized(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path)
    if not isinstance(data, dict):
        return [f"{path.name}: root must be object"]
    missing = sorted(REQUIRED_NORMALIZED_FIELDS - set(data))
    if missing:
        errors.append(f"{path.name}: missing fields: {', '.join(missing)}")
    limitations = data.get("limitations")
    if not isinstance(limitations, list) or not limitations:
        errors.append(f"{path.name}: limitations must be a non-empty list")
    return errors


def validate_manifest(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path)
    if not isinstance(data, dict):
        return [f"{path.name}: root must be object"]
    if data.get("not_official_codex_thread") is not True:
        errors.append(f"{path.name}: not_official_codex_thread must be true")
    return errors


def validate_timeline(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path.name}:{lineno}: invalid JSON: {exc}")
            continue
        if not isinstance(event, dict):
            errors.append(f"{path.name}:{lineno}: event must be object")
            continue
        if not event.get("type"):
            errors.append(f"{path.name}:{lineno}: missing type")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate sidechat protocol machine export")
    parser.add_argument("--export-dir", required=True, help="Folder containing manifest.json, normalized.json, timeline.jsonl")
    args = parser.parse_args()

    export_dir = pathlib.Path(args.export_dir)
    errors: list[str] = []

    normalized = export_dir / "normalized.json"
    timeline = export_dir / "timeline.jsonl"
    manifest = export_dir / "manifest.json"

    if not normalized.exists():
        errors.append(f"missing {normalized}")
    else:
        errors.extend(validate_normalized(normalized))

    if not timeline.exists():
        errors.append(f"missing {timeline}")
    else:
        errors.extend(validate_timeline(timeline))

    if manifest.exists():
        errors.extend(validate_manifest(manifest))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"OK sidechat export: {export_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
