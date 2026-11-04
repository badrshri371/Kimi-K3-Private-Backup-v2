# Download the official Kimi K3 snapshot

This repository does not host the model weights. Download them directly from the official Hugging Face repository to storage you control.

## Requirements

- Python 3.10 or newer
- A storage destination with enough free space for the entire snapshot
- A stable, high-bandwidth connection
- Hugging Face access accepted for the model, if the upstream repository requires it
- A Hugging Face account/token if authentication is required

Install the helper dependency:

```bash
python -m pip install -r requirements.txt
```

If the repository requires authentication, sign in using the official Hugging Face CLI:

```bash
hf auth login
```

Create a token through your Hugging Face account settings. Never put a token in this repository, a script, a commit, or a screenshot.

## Resolve and download

First check the upstream model page and license:

https://huggingface.co/moonshotai/Kimi-K3

Then run the script with a destination on a drive that has sufficient capacity:

```bash
python scripts/download_snapshot.py --destination /path/to/storage/Kimi-K3 --revision main --confirm-large-download
```

On Windows, for example:

```powershell
py -m pip install -r requirements.txt
hf auth login
py scripts/download_snapshot.py --destination E:\\ModelBackups\\Kimi-K3 --revision main --confirm-large-download
```

The script resolves the requested branch/tag/commit to an immutable commit SHA before downloading. It prints the estimated size when the upstream API provides it, downloads that exact revision, then writes `snapshot-manifest.json` into the destination.

The download can take a long time and may use a very large amount of bandwidth. Hugging Face's download library supports resuming cached downloads; do not delete its cache while a download is in progress.

## Pin an exact revision

For a long-term archival copy, record the resolved commit SHA printed by the script. Future restores should use that SHA rather than `main`, because `main` can change.

Example:

```bash
python scripts/download_snapshot.py --destination /path/to/storage/Kimi-K3 --revision YOUR_COMMIT_SHA --confirm-large-download
```

## After downloading

Run the verification procedure in [VERIFY.md](VERIFY.md). Then copy the entire snapshot directory, including `snapshot-manifest.json`, to a second independent storage location and verify that copy too.

Do not upload the model shards to this GitHub repository. GitHub is only for the small scripts, metadata, and documentation.
