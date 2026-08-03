import os
from pathlib import Path


def _write_secret(path: Path, content: str) -> None:
    """Write content to file, restricting both the file and its parent directory to owner-only on POSIX systems."""
    path.parent.mkdir(parents=True, exist_ok=True, mode=_SECRET_DIR_MODE)
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, _SECRET_FILE_MODE)
    with os.fdopen(fd, "w") as f:
        f.write(content)
    try:
        path.chmod(_SECRET_FILE_MODE)
        path.parent.chmod(_SECRET_DIR_MODE)
    except (OSError, NotImplementedError):
        # Windows does not support POSIX modes; chmod() will raise. Best-effort.
        pass

