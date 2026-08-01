
def _touch(name: str, *, dir_fd: int | None = None) -> None:
    if _SUPPORTS_DIR_FD and dir_fd is not None:
        os.utime(name, None, dir_fd=dir_fd)
    else:
        os.utime(name, None)

