
def attempt_chmod_verbose(path, mode):
    log.debug("changing mode of %s to %o", path, mode)
    try:
        chmod(path, mode)
    except OSError as e:  # pragma: no cover
        log.debug("chmod failed: %s", e)

