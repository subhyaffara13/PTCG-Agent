
def _break_stale_marker(  # noqa: PLR0911
    name: str,
    *,
    stale_threshold: float,
    now: float,
    dir_fd: int | None = None,
) -> bool:
    # Atomic break pattern: read → rename to unique break-name → re-verify → unlink. The rename gives us a
    # private name nobody else can touch; if the re-verify sees a newer mtime or a different token, the
    # legitimate holder's heartbeat fired between read and rename and we must abort (leaving the .break.*
    # file behind rather than rollback-renaming, because rollback is itself racy).
    read_result = _read_marker(name, dir_fd=dir_fd)
    if read_result is None:
        return False
    info_before, mtime_before = read_result
    if now - mtime_before <= stale_threshold:
        return False
    if info_before is None:
        _unlink(name, dir_fd=dir_fd)
        return True

    break_name = f"{name}{_BREAK_SUFFIX}.{os.getpid()}.{secrets.token_hex(16)}"
    try:
        if _SUPPORTS_DIR_FD and dir_fd is not None:
            os.rename(name, break_name, src_dir_fd=dir_fd, dst_dir_fd=dir_fd)
        else:
            Path(name).rename(break_name)
    except OSError:  # pragma: no cover - race where the marker vanishes between read and rename
        return False

    read_after = _read_marker(break_name, dir_fd=dir_fd)
    if read_after is None:  # pragma: no cover - race where a peer unlinks the break-name file
        return False
    info_after, mtime_after = read_after
    if info_after is None:  # pragma: no cover - content replaced post-rename by a racing peer
        _unlink(break_name, dir_fd=dir_fd)
        return True
    if not hmac.compare_digest(info_before.token, info_after.token):  # pragma: no cover - race only
        return False
    if mtime_after > mtime_before:  # pragma: no cover - heartbeat raced our rename
        return False
    _unlink(break_name, dir_fd=dir_fd)
    return True

