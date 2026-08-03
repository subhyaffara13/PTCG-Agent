import os
from typing import Callable

def _filenames_from(
    arg: str,
    *,
    predicate: Callable[[str], bool],
) -> Generator[str]:
    """Generate filenames from an argument.

    :param arg:
        Parameter from the command-line.
    :param predicate:
        Predicate to use to filter out filenames. If the predicate
        returns ``True`` we will exclude the filename, otherwise we
        will yield it. By default, we include every filename
        generated.
    :returns:
        Generator of paths
    """
    if predicate(arg):
        return

    if os.path.isdir(arg):
        for root, sub_directories, files in os.walk(arg):
            # NOTE(sigmavirus24): os.walk() will skip a directory if you
            # remove it from the list of sub-directories.
            for directory in tuple(sub_directories):
                joined = os.path.join(root, directory)
                if predicate(joined):
                    sub_directories.remove(directory)

            for filename in files:
                joined = os.path.join(root, filename)
                if not predicate(joined):
                    yield joined
    else:
        yield arg

