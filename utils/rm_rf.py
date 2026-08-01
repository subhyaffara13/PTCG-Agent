
def rm_rf(path: Path) -> None:
    """Remove the path contents recursively, even if some elements
    are read-only."""
    path = ensure_extended_length_path(path)
    onerror = partial(on_rm_rf_error, start_path=path)
    if sys.version_info >= (3, 12):
        shutil.rmtree(str(path), onexc=onerror)
    else:
        shutil.rmtree(str(path), onerror=onerror)

