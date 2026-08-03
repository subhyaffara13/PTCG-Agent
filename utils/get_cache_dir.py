import sys
from pathlib import Path


def get_cache_dir(file_path: Path) -> Path:
    """Return the cache directory to write .pyc files for the given .py file path."""
    if sys.pycache_prefix:
        # given:
        #   prefix = '/tmp/pycs'
        #   path = '/home/user/proj/test_app.py'
        # we want:
        #   '/tmp/pycs/home/user/proj'
        return Path(sys.pycache_prefix) / Path(*file_path.parts[1:-1])
    else:
        # classic pycache directory
        return file_path.parent / "__pycache__"


def get_cache_dir():
    return str(_get_cache_path())

