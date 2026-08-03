import sys

def _sigmasks_enum() -> str:
    """Generates the source code for the Sigmasks int enum."""
    if sys.platform != "win32":
        return """
    import enum
    class Sigmasks(enum.IntEnum):
        SIG_BLOCK   = enum.auto()
        SIG_UNBLOCK = enum.auto()
        SIG_SETMASK = enum.auto()
        """
    return ""

