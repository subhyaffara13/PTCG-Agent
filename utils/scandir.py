import os
from typing import Callable

def scandir(
    path: str | os.PathLike[str],
    sort_key: Callable[[os.DirEntry[str]], object] = lambda entry: entry.name,
) -> list[os.DirEntry[str]]:
    """Scan a directory recursively, in breadth-first order.

    The returned entries are sorted according to the given key.
    The default is to sort by name.
    If the directory does not exist, return an empty list.
    """
    entries = []
    # Attempt to create a scandir iterator for the given path.
    try:
        scandir_iter = os.scandir(path)
    except FileNotFoundError:
        # If the directory does not exist, return an empty list.
        return []
    # Use the scandir iterator in a context manager to ensure it is properly closed.
    with scandir_iter as s:
        for entry in s:
            try:
                entry.is_file()
            except OSError as err:
                if _ignore_error(err):
                    continue
                # Reraise non-ignorable errors to avoid hiding issues.
                raise
            entries.append(entry)
    entries.sort(key=sort_key)  # type: ignore[arg-type]
    return entries

