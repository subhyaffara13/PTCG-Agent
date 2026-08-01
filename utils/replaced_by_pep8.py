
def replaced_by_pep8(compat_name: str, fn: C) -> C:

    # Unwrap staticmethod/classmethod
    fn = getattr(fn, "__func__", fn)

    # (Presence of 'self' arg in signature is used by explain_exception() methods, so we take
    # some extra steps to add it if present in decorated function.)
    if ["self"] == list(inspect.signature(fn).parameters)[:1]:

        @wraps(fn)
        def _inner(self, *args, **kwargs):
            warnings.warn(
                f"{compat_name!r} deprecated - use {fn.__name__!r}",
                PyparsingDeprecationWarning,
                stacklevel=2,
            )
            return fn(self, *args, **kwargs)

    else:

        @wraps(fn)
        def _inner(*args, **kwargs):
            warnings.warn(
                f"{compat_name!r} deprecated - use {fn.__name__!r}",
                PyparsingDeprecationWarning,
                stacklevel=2,
            )
            return fn(*args, **kwargs)

    _inner.__doc__ = f"""
        .. deprecated:: 3.0.0
           Use :class:`{fn.__name__}` instead
        """
    _inner.__name__ = compat_name
    _inner.__annotations__ = fn.__annotations__
    if isinstance(fn, types.FunctionType):
        _inner.__kwdefaults__ = fn.__kwdefaults__  # type: ignore [attr-defined]
    elif isinstance(fn, type) and hasattr(fn, "__init__"):
        _inner.__kwdefaults__ = fn.__init__.__kwdefaults__  # type: ignore [misc,attr-defined]
    else:
        _inner.__kwdefaults__ = None  # type: ignore [attr-defined]
    _inner.__qualname__ = fn.__qualname__
    return cast(C, _inner)

