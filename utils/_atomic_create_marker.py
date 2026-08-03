import os

def _atomic_create_marker(name: str, token: str, *, dir_fd: int | None = None) -> None:
    # O_NOFOLLOW blocks the symlink-overwrite attack where an attacker pre-creates the marker path as a
    # symlink pointing at a victim file. Mode 0o600 keeps the token unreadable to other users.
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | _O_NOFOLLOW
    if _SUPPORTS_DIR_FD and dir_fd is not None:
        fd = os.open(name, flags, 0o600, dir_fd=dir_fd)
    else:
        fd = os.open(name, flags, 0o600)
    try:
        content = f"{token}\n{os.getpid()}\n{socket.gethostname()}\n".encode("ascii")
        os.write(fd, content)
    finally:
        os.close(fd)

