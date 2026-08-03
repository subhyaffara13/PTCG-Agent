import os
from typing import Any

def symlink_or_skip(
    src: os.PathLike[str] | str,
    dst: os.PathLike[str] | str,
    **kwargs: Any,
) -> None:
    """Make a symlink, or skip the test in case symlinks are not supported."""
    try:
        os.symlink(src, dst, **kwargs)
    except OSError as e:
        skip(f"symlinks not supported: {e}")

