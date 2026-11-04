# Storage boundaries and what GitHub can do

## GitHub's role in this project

Use this repository for source-controlled text and automation:

- backup instructions and recovery procedures
- scripts that download and verify a snapshot on storage you control
- upstream metadata inventory and immutable revision records
- workflow logs and status tracking
- tested inference notes

## What must not be stored here

Do not commit the Kimi K3 weight shards or a full model snapshot to Git. The upstream snapshot is approximately 1.56 TB according to the currently referenced file listing. This is far beyond practical Git repository use and normal GitHub file limits. Git LFS is not a sensible substitute for a multi-terabyte archival model.

The GitHub Actions workflow in this repository only reads upstream metadata and commits a small JSON inventory. It does not download weights into the runner, upload model artifacts, or create a complete model backup.

## Where the actual snapshot belongs

Use storage designed for very large objects, such as a local high-capacity disk/NAS or an object-storage bucket. Keep at least two independent verified copies. Record the exact upstream commit and preserve the generated SHA-256 manifest alongside the snapshot.

## Status language

- **Repository tooling complete:** documentation, helper scripts, and inventory automation are committed.
- **Inventory refreshed:** the metadata workflow has run successfully and updated `upstream-inventory.json`.
- **Snapshot downloaded:** every required upstream file is present in external storage.
- **Snapshot verified:** all manifest checks pass.
- **Backup complete:** a second independent copy has also been verified and a restore/inference test has been recorded.

Never describe the backup as complete based only on the GitHub repository or its inventory.
