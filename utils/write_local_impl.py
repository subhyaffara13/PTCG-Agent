import os

def write_local_impl(cache_key: str, pickled_code: bytes) -> tuple[str, int] | None:
    path = code_state_path(cache_key)

    if path is None:
        return None

    # If the user isn't misusing our API, we should have exclusive access to
    # this directory.  But it's not too hard

    tmp_path = path + ".tmp"
    lock_path = path + ".lock"
    # We /mostly/ don't need the lock but the tmp file could be clobbered
    # TODO: use a safe tempfile create to eliminate lock
    from torch.utils._filelock import FileLock

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with FileLock(lock_path, timeout=LOCK_TIMEOUT):
        with open(tmp_path, "wb") as f:
            f.write(pickled_code)
            size = f.tell()
        os.replace(tmp_path, path)
    return path, size

