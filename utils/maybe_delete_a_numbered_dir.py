
def maybe_delete_a_numbered_dir(path: Path) -> None:
    """Remove a numbered directory if its lock can be obtained and it does
    not seem to be in use."""
    path = ensure_extended_length_path(path)
    lock_path = None
    try:
        lock_path = create_cleanup_lock(path)
        parent = path.parent

        garbage = parent.joinpath(f"garbage-{uuid.uuid4()}")
        path.rename(garbage)
        rm_rf(garbage)
    except OSError:
        #  known races:
        #  * other process did a cleanup at the same time
        #  * deletable directory was found
        #  * process cwd (Windows)
        return
    finally:
        # If we created the lock, ensure we remove it even if we failed
        # to properly remove the numbered dir.
        if lock_path is not None:
            try:
                lock_path.unlink()
            except OSError:
                pass

