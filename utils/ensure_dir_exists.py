from pathlib import Path


def ensure_dir_exists(path: str | Path, mode: int = 0o777) -> None:
    """Ensure that a directory exists

    If it doesn't exist, try to create it, protecting against a race condition
    if another process is doing the same.
    The default permissions are determined by the current umask.
    """
    try:
        Path(path).mkdir(parents=True, mode=mode)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    if not Path(path).is_dir():
        msg = f"{path!r} exists but is not a directory"
        raise OSError(msg)

