
def _parse_lock_holder(content: str | None) -> tuple[int, str, int | None] | None:
    # A well-formed lock file is "<pid>\n<hostname>\n" with an optional "<creation_time>\n" third line on Windows.
    # Anything else — wrong line count, a non-integer PID or creation time, empty or unreadable content — is
    # unparsable; returning None lets the caller treat it as a malformed lock to self-heal rather than a holder.
    if not content or len(lines := content.strip().splitlines()) not in {2, 3}:
        return None
    try:
        pid = int(lines[0])
        creation_time = int(lines[2]) if len(lines) == 3 else None  # noqa: PLR2004
    except ValueError:
        return None
    # A pid outside the valid range is a malformed lock, not a holder. Without this, a non-positive pid
    # reaches os.kill() where 0 / -1 mean "the caller's own process group / every process" so a dead
    # holder reads as alive and the lock is never reclaimed, while an oversized pid raises OverflowError
    # (not OSError/ValueError) out of the self-heal path. _parse_marker_bytes already enforces this range.
    if not 1 <= pid <= 2**31 - 1:
        return None
    return pid, lines[1], creation_time

