# Verify a Kimi K3 snapshot

A download is not considered backed up until its files have been checked.

## Generate the manifest

The download script generates `snapshot-manifest.json` after a successful snapshot download. It contains the resolved upstream commit, relative file paths, sizes, and locally computed SHA-256 hashes.

If you move or copy the snapshot, keep the manifest with it.

## Verify every file

From the repository root, run:

```bash
python scripts/verify_manifest.py /path/to/storage/Kimi-K3/snapshot-manifest.json
```

On Windows:

```powershell
py scripts/verify_manifest.py E:\\ModelBackups\\Kimi-K3\\snapshot-manifest.json
```

The verifier checks that every listed file exists, has the expected size, and matches its SHA-256 hash. It also reports files in the snapshot directory that are not listed in the manifest. Extra files are reported but are not automatically deleted.

A full SHA-256 pass over a multi-terabyte snapshot can take hours. Keep the computer and storage device powered on until it finishes.

## Important limits

- A locally generated hash proves that a later copy matches the file that was hashed. It does not independently prove that the original download was authentic.
- Prefer upstream-provided checksums or file hashes when available, and preserve the upstream commit SHA.
- If a file fails verification, re-download that file or the complete snapshot from the same pinned commit, then regenerate and verify the manifest.
- Verify the second storage copy independently. Do not assume that a successful file copy means the copy is healthy.

Keep the verification output with your backup records.
