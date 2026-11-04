# Kimi K3 Private Backup

A reproducible backup and recovery workspace for the official Moonshot AI Kimi K3 open-weight model release.

## Upstream source

- Model repository: https://huggingface.co/moonshotai/Kimi-K3
- License: review the license supplied by the upstream model repository before copying, redistributing, or deploying the model.

## What belongs here

This Git repository is for small, versioned backup metadata and recovery tooling:

- upstream revision and file manifest
- download and integrity-verification scripts
- environment and inference setup notes
- recovery instructions and backup status

**Do not store the model weight shards in Git.** The full model snapshot is very large (approximately 1.56 TB based on the upstream file listing) and should be stored separately in suitable object storage or on local/offline drives. Keep at least two verified copies if long-term recovery matters.

## Backup status

- [ ] Record the exact upstream revision/commit to preserve.
- [ ] Generate a complete file manifest for that revision.
- [ ] Download all required model files to external storage.
- [ ] Verify every downloaded file against upstream checksums where provided; otherwise record locally generated SHA-256 hashes.
- [ ] Keep a second independent copy.
- [ ] Test loading the snapshot with a documented inference runtime.

A backup is not complete until the full required snapshot has been downloaded, verified, and independently copied.

## Important

This repository currently documents the backup plan. It does not itself contain the model weights, and no completed model snapshot is claimed.
