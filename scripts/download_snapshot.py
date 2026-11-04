#!/usr/bin/env python3
"""Download a complete Hugging Face model snapshot and create a SHA-256 manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import HfApi, snapshot_download

REPO_ID = "moonshotai/Kimi-K3"


def sha256_file(path: Path, chunk_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, help="Directory where the full snapshot will be stored")
    parser.add_argument("--revision", default="main", help="Hugging Face branch, tag, or commit (default: main)")
    parser.add_argument(
        "--confirm-large-download",
        action="store_true",
        help="Required acknowledgement that this may download a multi-terabyte model",
    )
    args = parser.parse_args()

    if not args.confirm_large_download:
        parser.error("This is a very large model. Review storage/bandwidth first, then add --confirm-large-download.")

    destination = Path(args.destination).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)

    api = HfApi()
    print(f"Checking {REPO_ID}@{args.revision} ...")
    info = api.model_info(REPO_ID, revision=args.revision, files_metadata=True)
    commit_sha = info.sha
    siblings = info.siblings or []

    total_size = 0
    known_sizes = 0
    for item in siblings:
        size = getattr(item, "size", None)
        if size is not None:
            total_size += int(size)
            known_sizes += 1

    print(f"Resolved immutable commit: {commit_sha}")
    print(f"Files listed by upstream: {len(siblings)}")
    if known_sizes:
        print(f"Estimated bytes from upstream metadata: {total_size:,}")
        print(f"Estimated decimal TB: {total_size / 1_000_000_000_000:.3f}")
    else:
        print("Upstream did not provide sizes for the listed files.")

    print("Downloading the complete repository snapshot. This may take a very long time.")
    snapshot_path = Path(
        snapshot_download(
            repo_id=REPO_ID,
            revision=commit_sha,
            local_dir=str(destination),
        )
    ).resolve()

    print("Download finished. Hashing every regular file to create the local manifest...")
    entries = []
    for path in sorted(p for p in snapshot_path.rglob("*") if p.is_file()):
        # Hugging Face may create local metadata in this folder; include all regular files
        # so the manifest accurately describes the directory being archived.
        relative = path.relative_to(snapshot_path).as_posix()
        size = path.stat().st_size
        entries.append({
            "path": relative,
            "size_bytes": size,
            "sha256": sha256_file(path),
        })
        print(f"Hashed: {relative} ({size:,} bytes)")

    manifest = {
        "schema_version": 1,
        "repo_id": REPO_ID,
        "revision": commit_sha,
        "requested_revision": args.revision,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "file_count": len(entries),
        "total_size_bytes": sum(item["size_bytes"] for item in entries),
        "hash_algorithm": "sha256",
        "files": entries,
    }

    manifest_path = snapshot_path / "snapshot-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest written: {manifest_path}")
    print("Next: run scripts/verify_manifest.py against this manifest, then make and verify a second copy.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted. Hugging Face's cache may allow the download to resume when rerun.", file=sys.stderr)
        raise SystemExit(130)
