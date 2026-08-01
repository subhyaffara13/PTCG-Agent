
def _frozen_delattrs(self, name):
    """
    Attached to frozen classes as __delattr__.
    """
    if isinstance(self, BaseException) and name == "__notes__":
        BaseException.__delattr__(self, name)
        return

    raise FrozenInstanceError

