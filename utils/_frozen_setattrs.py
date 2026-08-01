
def _frozen_setattrs(self, name, value):
    """
    Attached to frozen classes as __setattr__.
    """
    if isinstance(self, BaseException) and name in (
        "__cause__",
        "__context__",
        "__traceback__",
        "__suppress_context__",
        "__notes__",
    ):
        BaseException.__setattr__(self, name, value)
        return

    raise FrozenInstanceError

