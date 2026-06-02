#!/usr/bin/env python3
"""Audit Sidechat Protocol Pack consistency.

This script is intentionally conservative: by default it only reports drift.
Use --repair-index to repair 00_INDEX.md metadata lines without creating a new
semantic addendum.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


ADD_RE = re.compile(r"_PROTOCOL_ADDENDUM_(\d{3})\.md$", re.IGNORECASE)
STATUS_RE = re.compile(r"^Статус:\s*updated with addendum\s+\d{3}\s*$", re.MULTILINE)
LATEST_RE = re.compile(r"^latest_addendum:\s*\d{3}\s*$", re.MULTILINE)
LAST_AT_RE = re.compile(r"^last_updated_at:\s*.+$", re.MULTILINE)
LAST_HUMAN_RE = re.compile(r"^Последнее обновление:\s*.+$", re.MULTILINE)


def iso_now() -> str:
    local = dt.datetime.now().astimezone()
    return local.isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def find_project_root(protocol_dir: Path) -> Path:
    for parent in [protocol_dir, *protocol_dir.parents]:
        if (parent / ".CodexProtocolsForCurrentProject").exists():
            return parent
    return protocol_dir.parents[0]


def protocol_id_from_index(protocol_dir: Path) -> str:
    index = protocol_dir / "00_INDEX.md"
    if index.exists():
        text = read_text(index)
        match = re.search(r"(?:protocol_id|Protocol ID):\s*`([^`]+)`", text)
        if match:
            return match.group(1)
    return protocol_dir.name


def date_parts_from_protocol_id(protocol_id: str) -> tuple[str, str, str]:
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})_", protocol_id)
    if not match:
        today = dt.datetime.now().astimezone()
        return today.strftime("%Y"), today.strftime("%m"), today.strftime("%d")
    return match.group(1), match.group(2), match.group(3)


def addendum_numbers(protocol_dir: Path) -> list[int]:
    numbers: list[int] = []
    for path in protocol_dir.glob("*_PROTOCOL_ADDENDUM_*.md"):
        match = ADD_RE.search(path.name)
        if match:
            numbers.append(int(match.group(1)))
    return sorted(set(numbers))


def glob_names(folder: Path, pattern: str) -> list[str]:
    return sorted(path.name for path in folder.glob(pattern))


def check_triplet(protocol_dir: Path, nnn: str) -> dict:
    patterns = [
        f"*_PROTOCOL_ADDENDUM_{nnn}.md",
        f"*_DECISION_DIFF_{nnn}.md",
        f"*_RAW_TRANSCRIPT_DELTA_{nnn}.md",
    ]
    checks = []
    for pattern in patterns:
        names = glob_names(protocol_dir, pattern)
        checks.append({"pattern": pattern, "ok": bool(names), "names": names})
    return {"ok": all(item["ok"] for item in checks), "checks": checks}


def check_machine_export(project_root: Path, protocol_id: str, nnn: str) -> dict:
    year, month, day = date_parts_from_protocol_id(protocol_id)
    machine_dir = (
        project_root
        / ".CodexProtocolsForCurrentProject"
        / "sidechats"
        / year
        / month
        / day
        / protocol_id
    )
    patterns = [
        f"*_ADDENDUM_{nnn}_manifest.json",
        f"*_ADDENDUM_{nnn}_NORMALIZED_*.json",
        f"*_ADDENDUM_{nnn}_TIMELINE_*.jsonl",
    ]
    checks = []
    for pattern in patterns:
        names = glob_names(machine_dir, pattern) if machine_dir.exists() else []
        checks.append({"pattern": pattern, "ok": bool(names), "names": names})
    return {
        "folder": str(machine_dir),
        "ok": machine_dir.exists() and all(item["ok"] for item in checks),
        "checks": checks,
    }


def check_index(protocol_dir: Path, nnn: str, triplet_names: list[str]) -> dict:
    index = protocol_dir / "00_INDEX.md"
    if not index.exists():
        return {"ok": False, "exists": False}
    text = read_text(index)
    checks = {
        "exists": True,
        "status_ok": bool(re.search(rf"^Статус:\s*updated with addendum\s+{nnn}\s*$", text, re.MULTILINE)),
        "latest_field_ok": bool(re.search(rf"^latest_addendum:\s*{nnn}\s*$", text, re.MULTILINE)),
        "last_updated_at_exists": bool(LAST_AT_RE.search(text)),
        "human_last_updated_exists": bool(LAST_HUMAN_RE.search(text)),
        "lists_latest_files": all(name in text for name in triplet_names),
    }
    checks["ok"] = all(checks.values())
    return checks


def repair_index(protocol_dir: Path, nnn: str) -> bool:
    index = protocol_dir / "00_INDEX.md"
    if not index.exists():
        return False
    text = read_text(index)
    now = iso_now()
    status_line = f"Статус: updated with addendum {nnn}"
    latest_line = f"latest_addendum: {nnn}"
    last_at_line = f"last_updated_at: {now}"
    human_last_line = f"Последнее обновление: {now}"

    if STATUS_RE.search(text):
        text = STATUS_RE.sub(status_line, text, count=1)
    else:
        text = text.replace("\n", f"\n{status_line}\n", 1)

    if LATEST_RE.search(text):
        text = LATEST_RE.sub(latest_line, text, count=1)
    else:
        text = text.replace(status_line, f"{status_line}\n{latest_line}", 1)

    if LAST_AT_RE.search(text):
        text = LAST_AT_RE.sub(last_at_line, text, count=1)
    else:
        text = text.replace(latest_line, f"{latest_line}\n{last_at_line}", 1)

    if LAST_HUMAN_RE.search(text):
        text = LAST_HUMAN_RE.sub(human_last_line, text, count=1)
    else:
        text = text.replace(last_at_line, f"{last_at_line}\n{human_last_line}", 1)

    write_text(index, text)
    return True


def check_decisions_file(protocol_dir: Path, nnn: str) -> dict:
    path = protocol_dir / "05_DECISIONS_AND_TASKS.md"
    if not path.exists():
        return {"ok": False, "exists": False}
    text = read_text(path)
    headings = re.findall(rf"^##\s+Addendum\s+{nnn}\b", text, flags=re.MULTILINE)
    all_headings = re.findall(r"^##\s+Addendum\s+(\d{3})\b", text, flags=re.MULTILINE)
    ids = re.findall(r"^\|\s*([A-ZА-Я][A-ZА-Я0-9_-]+-\d{3,}|DECISION-[A-Z0-9_-]+)\s*\|", text, flags=re.MULTILINE)
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    return {
        "ok": bool(headings) and not duplicates,
        "exists": True,
        "has_latest_addendum_section": bool(headings),
        "duplicate_ids": duplicates,
        "duplicate_addendum_headings": sorted({item for item in all_headings if all_headings.count(item) > 1}),
    }


def check_registry(project_root: Path, protocol_id: str, nnn: str) -> dict:
    registry_dir = project_root / ".CodexProtocolsForCurrentProject" / "registry"
    jsonl = registry_dir / "sidechat_protocol_registry.jsonl"
    index = registry_dir / "sidechat_protocol_registry_index.json"
    latest_protocol_id = f"{protocol_id}_ADDENDUM_{nnn}"
    result = {
        "jsonl": str(jsonl),
        "index": str(index),
        "jsonl_has_latest": False,
        "index_has_latest": False,
        "index_latest_number_ok": False,
    }
    if jsonl.exists():
        result["jsonl_has_latest"] = latest_protocol_id in read_text(jsonl)
    if index.exists():
        text = read_text(index)
        result["index_has_latest"] = latest_protocol_id in text
        result["index_latest_number_ok"] = f'"latest_addendum_number": "{nnn}"' in text
    result["ok"] = all(
        [result["jsonl_has_latest"], result["index_has_latest"], result["index_latest_number_ok"]]
    )
    return result


def audit(protocol_dir: Path, project_root: Path | None, repair: bool) -> dict:
    protocol_dir = protocol_dir.resolve()
    project_root = (project_root or find_project_root(protocol_dir)).resolve()
    protocol_id = protocol_id_from_index(protocol_dir)
    nums = addendum_numbers(protocol_dir)
    latest = max(nums) if nums else None
    nnn = f"{latest:03d}" if latest is not None else None
    result = {
        "protocol_dir": str(protocol_dir),
        "project_root": str(project_root),
        "protocol_id": protocol_id,
        "latest_addendum": nnn,
        "skipped_numbers": [],
        "checks": {},
        "errors": [],
        "warnings": [],
    }
    if latest is None:
        result["warnings"].append("No PROTOCOL_ADDENDUM_NNN files found.")
        return result

    expected = list(range(2, latest + 1))
    result["skipped_numbers"] = [f"{num:03d}" for num in expected if num not in nums]

    triplet = check_triplet(protocol_dir, nnn)
    triplet_names = [name for item in triplet["checks"] for name in item["names"]]
    index = check_index(protocol_dir, nnn, triplet_names)
    decisions = check_decisions_file(protocol_dir, nnn)
    machine = check_machine_export(project_root, protocol_id, nnn)
    registry = check_registry(project_root, protocol_id, nnn)

    if repair and not index.get("ok"):
        repair_index(protocol_dir, nnn)
        index = check_index(protocol_dir, nnn, triplet_names)
        result["warnings"].append("00_INDEX.md metadata repaired.")

    result["checks"] = {
        "markdown_triplet": triplet,
        "index": index,
        "decisions": decisions,
        "machine_export": machine,
        "registry": registry,
    }

    for name, check in result["checks"].items():
        if not check.get("ok"):
            result["errors"].append(name)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol-dir", required=True)
    parser.add_argument("--project-root")
    parser.add_argument("--repair-index", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = audit(
        Path(args.protocol_dir),
        Path(args.project_root) if args.project_root else None,
        args.repair_index,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"protocol_id: {result['protocol_id']}")
        print(f"latest_addendum: {result['latest_addendum']}")
        for name, check in result["checks"].items():
            print(f"{name}: {'ok' if check.get('ok') else 'FAIL'}")
        if result["errors"]:
            print("errors: " + ", ".join(result["errors"]))
        if result["warnings"]:
            print("warnings: " + "; ".join(result["warnings"]))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
