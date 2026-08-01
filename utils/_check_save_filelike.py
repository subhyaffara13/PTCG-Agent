
def _check_save_filelike(f):
    if not _is_path(f) and not hasattr(f, "write"):
        raise AttributeError(
            "expected 'f' to be string, path, or a file-like object with "
            "a 'write' attribute"
        )

