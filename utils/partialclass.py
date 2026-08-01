
def partialclass(cls, *args, **kwargs):  # noqa: D103
    class NewCls(cls):
        __init__ = partialmethod(cls.__init__, *args, **kwargs)

    return NewCls

