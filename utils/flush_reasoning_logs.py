
def flush_reasoning_logs(
    buffer: List[dict],
    filepath: Path,
    log: logging.Logger,
) -> None:
    """
    Write all buffered log entries to *filepath*, merging with any
    existing entries already on disk.  Clears *buffer* on success.
    Protected by atomic file locking.
    """
    if not buffer:
        return

    with FileLock(filepath):
        try:
            logs = _read_existing_logs(filepath)
            logs.extend(buffer)
            filepath.write_text(json.dumps(logs, indent=2), encoding="utf-8")
            buffer.clear()
        except Exception as e:
            log.error(f"Failed to flush reasoning logs to {filepath}: {e}")


def flush_reasoning_logs(
    buffer: List[dict],
    filepath: Path,
    log: logging.Logger,
) -> None:
    """
    Write all buffered log entries to *filepath*, merging with any
    existing entries already on disk.  Clears *buffer* on success.
    Protected by atomic file locking.
    """
    if not buffer:
        return

    with FileLock(filepath):
        try:
            logs = _read_existing_logs(filepath)
            logs.extend(buffer)
            filepath.write_text(json.dumps(logs, indent=2), encoding="utf-8")
            buffer.clear()
        except Exception as e:
            log.error(f"Failed to flush reasoning logs to {filepath}: {e}")


def flush_reasoning_logs(
    buffer: List[dict],
    filepath: Path,
    log: logging.Logger,
) -> None:
    """
    Write all buffered log entries to *filepath*, merging with any
    existing entries already on disk.  Clears *buffer* on success.
    Protected by atomic file locking.
    """
    if not buffer:
        return

    with FileLock(filepath):
        try:
            logs = _read_existing_logs(filepath)
            logs.extend(buffer)
            filepath.write_text(json.dumps(logs, indent=2), encoding="utf-8")
            buffer.clear()
        except Exception as e:
            log.error(f"Failed to flush reasoning logs to {filepath}: {e}")

