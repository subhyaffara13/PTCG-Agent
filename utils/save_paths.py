
def save_paths():
    """Make sure ``sys.path``, ``sys.meta_path`` and ``sys.path_hooks`` are preserved"""
    prev = sys.path[:], sys.meta_path[:], sys.path_hooks[:]

    try:
        yield
    finally:
        sys.path, sys.meta_path, sys.path_hooks = prev

