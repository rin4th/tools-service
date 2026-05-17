"""Cleanup task — sweep generated tool outputs older than TTL.

Reads:
    STORAGE_DIR        default /storage
    OUTPUT_TTL_HOURS   default 24
    OUTPUT_DIR_NAME    default outputs

Operates only on STORAGE_DIR/OUTPUT_DIR_NAME. Avatars and uploads are
never touched.
"""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path

log = logging.getLogger("worker.cleanup")


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        log.warning("Invalid %s=%r, using default %d", name, raw, default)
        return default


def _outputs_dir() -> Path:
    storage = Path(os.getenv("STORAGE_DIR", "/storage"))
    name = os.getenv("OUTPUT_DIR_NAME", "outputs")
    return storage / name


def run() -> None:
    ttl_hours = _env_int("OUTPUT_TTL_HOURS", 24)
    cutoff = time.time() - (ttl_hours * 3600)

    target = _outputs_dir()
    if not target.is_dir():
        log.info("Skipping sweep — %s does not exist yet", target)
        return

    scanned = 0
    removed = 0
    freed_bytes = 0
    errors = 0

    for entry in target.iterdir():
        if not entry.is_file():
            continue
        scanned += 1
        try:
            mtime = entry.stat().st_mtime
        except OSError as exc:
            log.warning("Cannot stat %s: %s", entry.name, exc)
            errors += 1
            continue

        if mtime >= cutoff:
            continue

        try:
            size = entry.stat().st_size
            entry.unlink()
        except OSError as exc:
            log.warning("Cannot remove %s: %s", entry.name, exc)
            errors += 1
            continue

        removed += 1
        freed_bytes += size
        log.debug("Removed %s (mtime=%.0f, size=%d)", entry.name, mtime, size)

    log.info(
        "Sweep done — scanned=%d removed=%d freed=%s errors=%d ttl=%dh dir=%s",
        scanned,
        removed,
        _fmt_bytes(freed_bytes),
        errors,
        ttl_hours,
        target,
    )


def _fmt_bytes(n: int) -> str:
    if n < 1024:
        return f"{n}B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f}KB"
    if n < 1024 * 1024 * 1024:
        return f"{n / (1024 * 1024):.1f}MB"
    return f"{n / (1024 * 1024 * 1024):.2f}GB"
