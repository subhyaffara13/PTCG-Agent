
def _make_alias(fn, name):
    """
    This function defines an alias of another function and sets its __name__ argument.
    It also sets its __module__ argument to the module of the caller.
    Note that when naively doing `alias = fn`, we have that `alias.__name__ == "fn"`, and
    `alias.__module__ == fn.__module__`.
    """

    def _fn(*args, **kwargs):
        return fn(*args, **kwargs)

    _fn.__name__ = name
    _fn.__module__ = inspect.currentframe().f_back.f_globals["__name__"]  # type: ignore[union-attr]
    return _fn

