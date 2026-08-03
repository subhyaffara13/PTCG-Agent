import os
from pathlib import Path


def _make_cachedir(target: Path) -> None:
    """Create the pytest cache directory atomically with supporting files.

    Creates a temporary directory with README.md, .gitignore, and CACHEDIR.TAG,
    then atomically renames it to the target location. If another process wins
    the race, the temporary directory is cleaned up.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    path = Path(tempfile.mkdtemp(prefix="pytest-cache-files-", dir=target.parent))
    try:
        # Reset permissions to the default, see #12308.
        # Note: there's no way to get the current umask atomically, eek.
        umask = os.umask(0o022)
        os.umask(umask)
        path.chmod(0o777 - umask)

        for name, content in CACHEDIR_FILES.items():
            path.joinpath(name).write_bytes(content)

        path.rename(target)
    except OSError as e:
        # If 2 concurrent pytests both race to the rename, the loser
        # gets "Directory not empty" from the rename. In this case,
        # everything is handled so just continue after cleanup.
        # On Windows, the error is a FileExistsError which translates to EEXIST.
        if e.errno not in (errno.ENOTEMPTY, errno.EEXIST):
            raise
    finally:
        shutil.rmtree(path, ignore_errors=True)

