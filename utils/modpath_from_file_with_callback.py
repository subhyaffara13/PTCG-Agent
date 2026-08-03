import itertools
import os
import sys
from typing import Callable

def modpath_from_file_with_callback(
    filename: str,
    path: list[str] | None = None,
    is_package_cb: Callable[[str, list[str]], bool] | None = None,
) -> list[str]:
    filename = os.path.expanduser(_path_from_filename(filename))
    paths_to_check = sys.path.copy()
    if path:
        paths_to_check = path + paths_to_check
    for pathname in itertools.chain(
        paths_to_check, map(_cache_normalize_path, paths_to_check)
    ):
        if not pathname:
            continue
        modpath = _get_relative_base_path(filename, pathname)
        if not modpath:
            continue
        assert is_package_cb is not None
        if is_package_cb(pathname, modpath[:-1]):
            return modpath

    raise ImportError(
        "Unable to find module for {} in {}".format(
            filename, ", \n".join(paths_to_check)
        )
    )

