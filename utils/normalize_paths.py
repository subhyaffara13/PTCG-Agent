import os

def normalize_paths(value, parent=os.curdir):
    """Parse a comma-separated list of paths.

    Return a list of absolute paths.
    """
    if not value:
        return []
    if isinstance(value, list):
        return value
    paths = []
    for path in value.split(','):
        path = path.strip()
        if '/' in path:
            path = os.path.abspath(os.path.join(parent, path))
        paths.append(path.rstrip('/'))
    return paths


def normalize_paths(
    paths: Sequence[str], parent: str = os.curdir
) -> list[str]:
    """Normalize a list of paths relative to a parent directory.

    :returns:
        The normalized paths.
    """
    assert isinstance(paths, list), paths
    return [normalize_path(p, parent) for p in paths]


def normalize_paths(paths):
  """Returns the list of normalized path."""
  # e.g. ["//absl/strings:dir/header.h"] -> ["absl/strings/dir/header.h"]
  return [path.lstrip("/").replace(":", "/") for path in paths]

