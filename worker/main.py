"""Tools-service worker.

Lightweight scheduler that runs maintenance tasks periodically.
No external deps — uses stdlib only.

Usage:
    python -m worker.main
"""

from __future__ import annotations

import logging
import os
import signal
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass

from worker.tasks import cleanup


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        logging.warning("Invalid %s=%r, using default %d", name, raw, default)
        return default


def _setup_logging() -> None:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-7s [%(name)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        stream=sys.stdout,
    )


@dataclass
class Job:
    name: str
    fn: Callable[[], None]
    interval_seconds: int
    next_run: float = 0.0


_running = True


def _on_signal(signum: int, _frame) -> None:  # noqa: ANN001
    global _running
    logging.info("Received signal %d, shutting down", signum)
    _running = False


def main() -> int:
    _setup_logging()
    log = logging.getLogger("worker")

    sweep_interval_min = _env_int("SWEEP_INTERVAL_MINUTES", 15)

    jobs: list[Job] = [
        Job(
            name="cleanup-outputs",
            fn=cleanup.run,
            interval_seconds=sweep_interval_min * 60,
        ),
    ]

    log.info(
        "Worker started — %d job(s), sweep_interval=%dm",
        len(jobs),
        sweep_interval_min,
    )

    signal.signal(signal.SIGTERM, _on_signal)
    signal.signal(signal.SIGINT, _on_signal)

    # Run each job once on startup, then on schedule
    while _running:
        now = time.monotonic()
        next_due = float("inf")

        for job in jobs:
            if now >= job.next_run:
                started = time.monotonic()
                try:
                    job.fn()
                except Exception:
                    log.exception("Job %s failed", job.name)
                else:
                    log.debug(
                        "Job %s completed in %.2fs",
                        job.name,
                        time.monotonic() - started,
                    )
                job.next_run = time.monotonic() + job.interval_seconds
            next_due = min(next_due, job.next_run)

        # Sleep in small slices so SIGTERM is responsive
        sleep_for = max(0.5, min(next_due - time.monotonic(), 5.0))
        time.sleep(sleep_for)

    log.info("Worker stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
