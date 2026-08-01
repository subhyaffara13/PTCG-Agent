
def _remove_sharing_cache() -> None:
    tid = threading.get_ident()
    _SHARING_STACK[tid].pop()
    if not _SHARING_STACK[tid]:
        del _SHARING_STACK[tid]

