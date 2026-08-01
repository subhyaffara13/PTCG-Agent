
def TerminalReporter_startdir(self: TerminalReporter) -> LEGACY_PATH:
    """The directory from which pytest was invoked.

    Prefer to use ``startpath`` which is a :class:`pathlib.Path`.

    :type: LEGACY_PATH
    """
    return legacy_path(self.startpath)

