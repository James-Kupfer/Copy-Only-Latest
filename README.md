# copy_only_latest

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A minimal Python utility that consolidates one or more source directory
trees into a destination root, copying only files that are **newer** than
what already exists at the destination.

Useful for merging a restored or backup tree back into a live directory
without overwriting files that are already current.

---

## Features

- Copies a file only when the source is newer than the destination.
- Skips files where the destination is the same age or newer.
- Preserves the relative directory structure of each source folder.
- Prevents accidental self-copies when source and destination paths overlap.
- Prints each copied file and a final summary of copied / skipped / errors.

---

## Requirements

- Python 3.7+ (standard library only)
- No Windows dependency — the code itself is OS-portable (uses `os.walk` /
  `shutil.copy2`), though the example paths below are Windows-style since
  that's this tool's primary use case.

---

## Configuration

```bash
git clone https://github.com/James-Kupfer/Copy-Only-Latest.git
cd Copy-Only-Latest
```

Open `copy_only_latest.py` and edit the two variables near the top of the
file — these are the **only lines you need to change**:

```python
# One or more source directories to consolidate
SRC_FOLDERS: List[str] = [
    r"C:\restore\C_\Documents",
]

# Destination root -- files are copied here preserving relative paths
DST_ROOT: str = r"C:\Documents"
```

Multiple source folders are supported:

```python
SRC_FOLDERS: List[str] = [
    r"C:\restore\C_\Documents",
    r"C:\restore\C_\Beaker",
]
```

---

## Usage

```cmd
python copy_only_latest.py
```

Example output:

```text
COPIED: C:\restore\C_\Documents\report.docx -> C:\Documents\report.docx
COPIED: C:\restore\C_\Documents\notes\2025.txt -> C:\Documents\notes\2025.txt

Done: 2 copied, 118 skipped, 0 errors.
```

- **COPIED** -- source was newer; destination was updated.
- **Skipped** -- destination was the same age or newer; no action taken.
- **Errors** -- file could not be read or written (e.g. locked or missing).

---

## Using it from other scripts

```python
from copy_only_latest import consolidate

consolidate()
```

`SRC_FOLDERS` and `DST_ROOT` are module-level variables, so you can
override them before calling `consolidate()` if needed:

```python
import copy_only_latest as col

col.SRC_FOLDERS = [r"D:\backup\Documents"]
col.DST_ROOT    = r"C:\Documents"
col.consolidate()
```

---

## License

Apache License 2.0 — see [LICENSE](LICENSE).
