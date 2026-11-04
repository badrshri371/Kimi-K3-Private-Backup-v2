# Kimi K3 Private Backup

A reproducible backup and recovery workspace for the official Moonshot AI Kimi K3 open-weight model release.

## Upstream source

- Model repository: https://huggingface.co/moonshotai/Kimi-K3
- License: review the license supplied by the upstream model repository before copying, redistributing, or deploying the model.

## Repository contents

- [Backup plan](BACKUP_PLAN.md)
- [Download instructions](DOWNLOAD.md)
- [Integrity verification](VERIFY.md)
- [Inference preparation](INFERENCE.md)
- [Python dependencies](requirements.txt)
- [Snapshot downloader](scripts/download_snapshot.py)
- [SHA-256 verifier](scripts/verify_manifest.py)

## Important storage rule

**Do not store the model weight shards in Git.** The full model snapshot is very large (approximately 1.56 TB based on the upstream file listing) and should be stored separately in suitable object storage or on local/offline drives. Keep at least two verified copies if long-term recovery matters.

## Backup status

- [x] Create repository documentation and helper scripts.
- [ ] Record the exact upstream revision/commit to preserve.
- [ ] Download all required model files to external storage.
- [ ] Generate and verify the complete SHA-256 manifest.
- [ ] Keep a second independent copy and verify it.
- [ ] Test loading the snapshot with a documented inference runtime.

A backup is not complete until the full required snapshot has been downloaded, verified, and independently copied.

## Current status

This repository contains the backup plan and tooling only. It does not contain the Kimi K3 weights, and no completed model snapshot is claimed.
