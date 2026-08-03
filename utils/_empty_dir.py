import os

def _empty_dir(dir_: _P) -> _P:
    """Create a directory ensured to be empty. Existing files may be removed."""
    _shutil.rmtree(dir_, ignore_errors=True)
    os.makedirs(dir_)
    return dir_

