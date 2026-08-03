import itertools
from pathlib import Path


def resolve_package_path(path: Path) -> Path | None:
    """Return the Python package path by looking for the last
    directory upwards which still contains an __init__.py.

    Returns None if it cannot be determined.
    """
    result = None
    for parent in itertools.chain((path,), path.parents):
        if parent.is_dir():
            if not (parent / "__init__.py").is_file():
                break
            if not parent.name.isidentifier():
                break
            result = parent
    return result

