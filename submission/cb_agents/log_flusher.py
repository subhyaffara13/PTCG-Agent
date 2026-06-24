"""
agents/log_flusher.py

Shared utility for flushing in-memory reasoning log buffers to JSON files.
Handles reading existing logs, merging, and writing back atomically.
"""

import json
import logging
from pathlib import Path
from typing import List


def flush_reasoning_logs(
    buffer: List[dict],
    filepath: Path,
    log: logging.Logger,
) -> None:
    """
    Write all buffered log entries to *filepath*, merging with any
    existing entries already on disk.  Clears *buffer* on success.

    Parameters
    ----------
    buffer : list[dict]
        In-memory log entries to persist.
    filepath : Path
        Target JSON file (created if absent).
    log : logging.Logger
        Logger used for error reporting.
    """
    if not buffer:
        return

    try:
        logs = _read_existing_logs(filepath)
        logs.extend(buffer)
        filepath.write_text(json.dumps(logs, indent=2), encoding="utf-8")
        buffer.clear()
    except Exception as e:
        log.error(f"Failed to flush reasoning logs to {filepath}: {e}")


def _read_existing_logs(filepath: Path) -> list:
    """Return the list of log entries already stored in *filepath*."""
    if not filepath.exists():
        return []

    content = filepath.read_text(encoding="utf-8").strip()
    if not content:
        return []

    try:
        data = json.loads(content)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        return []
