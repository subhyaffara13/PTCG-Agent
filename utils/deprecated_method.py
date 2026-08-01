
def deprecated_method(replacement):
    """A decorator which can be used to mark a method as deprecated
    'replcement' is the method name which will be called instead.
    """

    def outer(fun):
        msg = (
            f"{fun.__name__}() is deprecated and will be removed; use"
            f" {replacement}() instead"
        )
        if fun.__doc__ is None:
            fun.__doc__ = msg

        @functools.wraps(fun)
        def inner(self, *args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            return getattr(self, replacement)(*args, **kwargs)

        return inner

    return outer


def deprecated_method(method: t.Any, cls: t.Any, method_name: str, msg: str) -> None:
    """Show deprecation warning about a magic method definition.

    Uses warn_explicit to bind warning to method definition instead of triggering code,
    which isn't relevant.
    """
    warn_msg = f"{cls.__name__}.{method_name} is deprecated in traitlets 4.1: {msg}"

    for parent in inspect.getmro(cls):
        if method_name in parent.__dict__:
            cls = parent
            break
    # limit deprecation messages to once per package
    package_name = cls.__module__.split(".", 1)[0]
    key = (package_name, msg)
    if not should_warn(key):
        return
    try:
        fname = inspect.getsourcefile(method) or "<unknown>"
        lineno = inspect.getsourcelines(method)[1] or 0
    except (OSError, TypeError) as e:
        # Failed to inspect for some reason
        warn(
            warn_msg + ("\n(inspection failed) %s" % e),
            DeprecationWarning,
            stacklevel=2,
        )
    else:
        warnings.warn_explicit(warn_msg, DeprecationWarning, fname, lineno)

