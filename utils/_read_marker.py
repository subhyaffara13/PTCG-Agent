
def _read_marker(name: str, *, dir_fd: int | None = None) -> tuple[_MarkerInfo | None, float] | None:
    # The file is ours; these guard a hostile mid-flight swap. O_NOFOLLOW rejects a symlink; O_NONBLOCK keeps
    # a real FIFO from blocking the open forever, so it reads as a malformed marker instead of wedging a peer
    # that holds the state lock.
    flags = os.O_RDONLY | _O_NOFOLLOW | _O_NONBLOCK
    try:
        fd = os.open(name, flags, dir_fd=dir_fd) if _SUPPORTS_DIR_FD and dir_fd is not None else os.open(name, flags)
    except OSError:
        return None
    try:
        try:
            st = os.fstat(fd)
            data = os.read(fd, _MAX_MARKER_SIZE + 1)
        except OSError:  # pragma: no cover - e.g. EAGAIN from a hostile FIFO that has a writer attached
            return None
    finally:
        os.close(fd)
    return _parse_marker_bytes(data), st.st_mtime

