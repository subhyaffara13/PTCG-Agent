
def _register_hooks() -> None:
    global _atexit_registered, _fork_registered  # noqa: PLW0603
    if not _atexit_registered:
        atexit.register(_cleanup_all_instances)
        _atexit_registered = True
    # after_in_child replaces inherited state so the child cannot double-own any lock the parent held.
    if not _fork_registered and hasattr(os, "register_at_fork"):
        os.register_at_fork(after_in_child=_reset_all_after_fork)
        _fork_registered = True

