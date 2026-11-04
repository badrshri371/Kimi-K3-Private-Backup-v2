#!/usr/bin/env python3
"""Record the official Kimi K3 repository's file metadata without downloading weights."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import HfApi

REPO_ID = "moonshotai/Kimi-K3"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default="main", help="Branch, tag, or commit to inspect")
    parser.add_argument("--output", default="upstream-inventory.json", help="Output JSON path")
    args = parser.parse_args()

    api = HfApi()
    info = api.model_info(REPO_ID, revision=args.revision, files_metadata=True)
    files = []
    total_bytes = 0
    known_size_count = 0

    for item in sorted(info.siblings or [], key=lambda entry: entry.rfilename):
        lfs = getattr(item, "lfs", None)
        size = getattr(item, "size", None)
        if size is not None:
            total_bytes += int(size)
            known_size_count += 1
        files.append({
            "path": item.rfilename,
            "size_bytes": int(size) if size is not None else None,
            "lfs": lfs if isinstance(lfs, dict) else (lfs.__dict__ if lfs else None),
        })

    inventory = {
        "schema_version": 1,
        "repo_id": REPO_ID,
        "requested_revision": args.revision,
        "resolved_commit": info.sha,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "file_count": len(files),
        "known_size_file_count": known_size_count,
        "known_total_size_bytes": total_bytes if known_size_count else None,
        "files": files,
        "note": "Metadata inventory only. No model weights are downloaded or stored in this Git repository.",
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Inventory written to {output}")
    print(f"Resolved commit: {info.sha}")
    print(f"Files listed: {len(files)}")
    if known_size_count:
        print(f"Known total size: {total_bytes:,} bytes ({total_bytes / 1_000_000_000_000:.3f} decimal TB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
