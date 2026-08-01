
def Session_startdir(self: Session) -> LEGACY_PATH:
    """The path from which pytest was invoked.

    Prefer to use ``startpath`` which is a :class:`pathlib.Path`.

    :type: LEGACY_PATH
    """
    return legacy_path(self.startpath)

