"""copy_only_latest.py

Copies files from one or more source folders into a destination root,
but only when the source file is **newer** than the existing destination
file.  If the destination file does not exist it is always copied.

This is useful for consolidating a restored or backup tree into a live
directory without overwriting files that are already up to date.

Configuration
-------------
Edit ``SRC_FOLDERS`` and ``DST_ROOT`` at the top of this file before
running.  No other changes are required.

Output
------
Each copied file is printed as ``COPIED: <src> -> <dst>``.
A summary line is printed on completion::

    Done: 12 copied, 45 skipped, 0 errors.
"""

import os
import shutil
from typing import List

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

#: Source directories to consolidate. Each is walked recursively and its
#: relative structure is preserved under DST_ROOT.
SRC_FOLDERS: List[str] = [
    r"C:\restore\C\Documents",
]

#: Destination root. Files are copied here preserving relative paths.
DST_ROOT: str = r"C:\Documents"


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def consolidate() -> None:
    """Copy newer source files into DST_ROOT, skipping unchanged files.

    For each file found under any folder in ``SRC_FOLDERS``:

    - If the destination does not exist, the file is copied.
    - If the destination exists and the source is **newer**, the file is
      copied (overwriting the destination).
    - If the destination exists and is the same age or newer, the file is
      skipped.

    Files whose resolved destination path falls inside a source folder
    are always skipped to prevent self-copies.
    """
    copied = skipped = errors = 0

    for src_root in SRC_FOLDERS:
        if not os.path.exists(src_root):
            print(f"SKIP (not found): {src_root}")
            continue

        for dirpath, _, filenames in os.walk(src_root):
            for fname in filenames:
                src = os.path.join(dirpath, fname)
                rel = os.path.relpath(src, src_root)
                dst = os.path.join(DST_ROOT, rel)

                # Prevent self-copy if DST_ROOT overlaps a source folder
                dst_abs = os.path.abspath(dst)
                if any(
                    dst_abs.startswith(os.path.abspath(s)) for s in SRC_FOLDERS
                ):
                    continue

                try:
                    src_mtime = os.path.getmtime(src)

                    if os.path.exists(dst):
                        if src_mtime <= os.path.getmtime(dst):
                            skipped += 1
                            continue  # destination is same age or newer

                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)
                    copied += 1
                    print(f"COPIED: {src} -> {dst}")

                except OSError as e:
                    print(f"ERROR: {src}: {e}")
                    errors += 1

    print(f"\nDone: {copied} copied, {skipped} skipped, {errors} errors.")


if __name__ == "__main__":
    consolidate()
