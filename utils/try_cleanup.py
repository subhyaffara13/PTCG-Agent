
def try_cleanup(path: Path, consider_lock_dead_if_created_before: float) -> None:
    """Try to cleanup a directory if we can ensure it's deletable."""
    if ensure_deletable(path, consider_lock_dead_if_created_before):
        maybe_delete_a_numbered_dir(path)

