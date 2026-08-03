import os
from pathlib import Path


def _unlink(name: str, *, dir_fd: int | None = None) -> None:
    with suppress(FileNotFoundError):
        if _SUPPORTS_DIR_FD and dir_fd is not None:
            # Path.unlink has no dir_fd support, so we stay on os.unlink for the dirfd path.
            os.unlink(name, dir_fd=dir_fd)
        else:
            Path(name).unlink()

