
def remove_tree(directory, verbose=True):
    """Recursively remove an entire directory tree.

    Any errors are ignored (apart from being reported to stdout if 'verbose'
    is true).
    """
    if verbose >= 1:
        log.info("removing '%s' (and everything under it)", directory)
    cmdtuples = []
    _build_cmdtuple(directory, cmdtuples)
    for cmd in cmdtuples:
        try:
            cmd[0](cmd[1])
            # Clear the cache
            SkipRepeatAbsolutePaths.clear()
        except OSError as exc:
            log.warning("error removing %s: %s", directory, exc)

