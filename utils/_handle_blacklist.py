
def _handle_blacklist(
    blacklist: Sequence[str], dirnames: list[str], filenames: list[str]
) -> None:
    """Remove files/directories in the black list.

    dirnames/filenames are usually from os.walk
    """
    for norecurs in blacklist:
        if norecurs in dirnames:
            dirnames.remove(norecurs)
        elif norecurs in filenames:
            filenames.remove(norecurs)

