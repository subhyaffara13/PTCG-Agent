import os

def sorted_walk(
    dir: GenericPath[AnyStr],
) -> Iterator[tuple[AnyStr, list[AnyStr], list[AnyStr]]]:
    """Do os.walk in a reproducible way,
    independent of indeterministic filesystem readdir order
    """
    for base, dirs, files in os.walk(dir):
        dirs.sort()
        files.sort()
        yield base, dirs, files

