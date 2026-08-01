
def _read_lock_file(path: str) -> tuple[str | None, float, int]:
    # The lock file is created with O_EXCL | O_NOFOLLOW, so a symlink here is a hostile replacement and must
    # not be followed. O_NONBLOCK keeps an attacker-placed FIFO from stalling the open (O_NOFOLLOW alone only
    # rejects a symlink, not a real FIFO at the path), and the capped read stops a huge file (e.g. /dev/zero)
    # from exhausting memory. Content is None when the file is too large or not UTF-8, but the mtime and inode
    # still flow back so the caller can evict it as a stale, malformed lock and verify identity before breaking.
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    try:
        st, data = os.fstat(fd), os.read(fd, _MAX_LOCK_FILE_SIZE + 1)
    finally:
        os.close(fd)
    if len(data) <= _MAX_LOCK_FILE_SIZE:
        with suppress(UnicodeDecodeError):
            return data.decode("utf-8"), st.st_mtime, st.st_ino
    return None, st.st_mtime, st.st_ino

