
def _do_i_own(path: str) -> bool:
    """Return whether the current user owns the given path"""
    p = Path(path).resolve()

    # walk up to first existing parent
    while not p.exists() and p != p.parent:
        p = p.parent

    # simplest check: owner by name
    # not always implemented or available
    try:
        return p.owner() == os.getlogin()
    except Exception:  # noqa: S110
        pass

    if hasattr(os, "geteuid"):
        try:
            st = p.stat()
            return st.st_uid == os.geteuid()
        except (NotImplementedError, OSError):
            # geteuid not always implemented
            pass

    # no ownership checks worked, check write access
    return os.access(p, os.W_OK)

