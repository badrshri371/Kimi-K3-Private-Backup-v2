# Backup and recovery plan

## Goal

Preserve a reproducible copy of the official Kimi K3 model release so it can be restored and run later, even if the upstream hosting page changes.

## What must be preserved for inference

At minimum, preserve the complete model repository snapshot at one immutable upstream commit:

- all model weight shards
- model configuration and generation configuration
- tokenizer files and vocabularies
- model-specific Python/configuration files supplied by the repository
- any other files required by the model's documented inference path

Do not assume that saving only the weight files is sufficient.

## Where to store it

Use this GitHub repository for small text files, scripts, manifests, and documentation only. Do not upload multi-terabyte weight files to GitHub.

Store the downloaded snapshot on a filesystem or object-storage service that can handle files of this size. Keep a second copy on a separate device or storage account. A second folder on the same physical drive is not an independent backup.

Before downloading, check that the destination has enough free space for the complete snapshot plus temporary files and future updates. Use a filesystem and storage provider that support the largest individual shard.

## Reproducibility record

For every backup, record:

1. Upstream repository: `moonshotai/Kimi-K3`
2. Exact upstream commit SHA (not just the moving `main` branch)
3. Download date in UTC
4. Local destination and storage medium
5. File count and total bytes
6. SHA-256 for every downloaded file
7. Inference runtime, version, and tested command
8. Whether a second independent copy was verified

The download script resolves the selected upstream revision to a commit SHA and downloads that exact revision. Keep the generated `snapshot-manifest.json` with the snapshot.

## Completion checklist

- [ ] Confirm the upstream model license and usage conditions.
- [ ] Resolve and record the exact upstream commit.
- [ ] Check storage capacity and network limits.
- [ ] Download the complete snapshot.
- [ ] Generate the SHA-256 manifest.
- [ ] Run the verification script successfully.
- [ ] Copy the snapshot and manifest to separate storage.
- [ ] Verify the second copy.
- [ ] Test loading the preserved snapshot with a compatible inference engine.
- [ ] Record the tested runtime and hardware.

A README or download script is not a model backup. The backup is complete only after all required files have been downloaded, verified, and copied independently.
