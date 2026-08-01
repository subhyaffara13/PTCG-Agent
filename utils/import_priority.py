
def import_priority(imp: ImportBase, toplevel_priority: int) -> int:
    """Compute import priority from an import node."""
    if not imp.is_top_level:
        # Inside a function
        return PRI_LOW
    if imp.is_mypy_only:
        # Inside "if MYPY" or "if typing.TYPE_CHECKING"
        return max(PRI_MYPY, toplevel_priority)
    # A regular import; priority determined by argument.
    return toplevel_priority

