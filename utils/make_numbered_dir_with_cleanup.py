
def make_numbered_dir_with_cleanup(
    *,
    root: Path,
    prefix: str,
    mode: int,
    keep: int,
    lock_timeout: float,
    register: Any,
) -> Path:
    """Create a numbered dir and register its cleanup.

    Similar to make_numbered_dir, but also maintains a lock file indicating that
    the directory is currently in use, and registers the cleanup of the lock and
    of stale numbered directories.

    :param keep:
        The number of sessions to retain the directory.
    :param lock_timeout:
        In case of a crash, the lock remains "stuck". The timeout is a time
        limit after which the lock is considered stale and can be removed.
    :param register:
        Called as register(cleanup_func, params...). Should schedule to call
        passed cleanup functions on session finish.
    """
    e = None
    for i in range(10):
        try:
            p = make_numbered_dir(root, prefix, mode)
            # Only lock the current dir when keep is not 0
            if keep != 0:
                lock_path = create_cleanup_lock(p)
                register_cleanup_lock_removal(lock_path, register)
        except Exception as exc:
            e = exc
        else:
            consider_lock_dead_if_created_before = p.stat().st_mtime - lock_timeout
            # Register a cleanup for program exit
            register(
                cleanup_numbered_dir,
                root,
                prefix,
                keep,
                consider_lock_dead_if_created_before,
            )
            return p
    assert e is not None
    raise e

