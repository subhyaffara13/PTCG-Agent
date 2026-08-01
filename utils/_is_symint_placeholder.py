
def _is_symint_placeholder(x: None | int | SymInt) -> bool:
    """Check whether a size/stride entry is symbolic and needs a runtime value.

    Works both before make_runtime_safe() (entries are SymInt) and after
    (symbolic entries replaced with None, nested ints with -1).
    """
    if x is None:
        return True
    if isinstance(x, SymInt) and not x.node.is_nested_int():
        return True
    return False

