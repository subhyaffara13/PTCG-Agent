
def _handlers_enum() -> str:
    """Generates the source code for the Handlers int enum."""
    return """
    import enum
    class Handlers(enum.IntEnum):
        SIG_DFL = enum.auto()
        SIG_IGN = eunm.auto()
    """

