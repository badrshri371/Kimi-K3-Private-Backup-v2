#!/usr/bin/env python3
"""Verify file sizes and SHA-256 hashes recorded in snapshot-manifest.json."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256_file(path: Path, chunk_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Path to snapshot-manifest.json")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    if not manifest_path.is_file():
        parser.error(f"Manifest not found: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    root = manifest_path.parent
    records = manifest.get("files")
    if not isinstance(records, list):
        parser.error("Manifest does not contain a valid 'files' list.")

    failures = []
    listed_paths = set()
    total = len(records)

    print(f"Repository: {manifest.get('repo_id', 'unknown')}")
    print(f"Revision:   {manifest.get('revision', 'unknown')}")
    print(f"Checking {total} files under {root}")

    for index, record in enumerate(records, start=1):
        relative = record.get("path")
        if not isinstance(relative, str) or not relative:
            failures.append(f"Invalid path in manifest entry {index}")
            continue

        file_path = (root / relative).resolve()
        try:
            file_path.relative_to(root)
        except ValueError:
            failures.append(f"Unsafe path outside snapshot: {relative}")
            continue

        listed_paths.add(relative)
        if not file_path.is_file():
            failures.append(f"MISSING: {relative}")
            continue

        actual_size = file_path.stat().st_size
        expected_size = int(record["size_bytes"])
        if actual_size != expected_size:
            failures.append(f"SIZE MISMATCH: {relative} expected {expected_size}, got {actual_size}")
            continue

        actual_hash = sha256_file(file_path)
        expected_hash = record["sha256"]
        if actual_hash.lower() != str(expected_hash).lower():
            failures.append(f"HASH MISMATCH: {relative}")
        else:
            print(f"[{index}/{total}] OK {relative}")

    extras = []
    for path in root.rglob("*"):
        if path.is_file() and path.name != manifest_path.name:
            relative = path.relative_to(root).as_posix()
            if relative not in listed_paths:
                extras.append(relative)

    if extras:
        print(f"\nUnlisted files found ({len(extras)}); they were not deleted:")
        for item in extras:
            print(f"  EXTRA: {item}")

    if failures:
        print(f"\nFAILED: {len(failures)} problem(s):", file=sys.stderr)
        for item in failures:
            print(f"  {item}", file=sys.stderr)
        return 1

    print(f"\nSUCCESS: all {total} manifest entries match their recorded size and SHA-256.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Verification error: {exc}", file=sys.stderr)
        raise SystemExit(2)
