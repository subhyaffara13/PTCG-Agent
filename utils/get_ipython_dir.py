import os
from pathlib import Path


def get_ipython_dir() -> str:
    """Return the IPython directory location.

    Not imported from IPython because the IPython implementation
    ensures that a writable directory exists,
    creating a temporary directory if not.
    We don't want to trigger that when checking if migration should happen.

    We only need to support the IPython < 4 behavior for migration,
    so importing for forward-compatibility and edge cases is not important.
    """
    return os.environ.get("IPYTHONDIR", str(Path("~/.ipython").expanduser()))

