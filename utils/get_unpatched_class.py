
def get_unpatched_class(cls: type[_T]) -> type[_T]:
    """Protect against re-patching the distutils if reloaded

    Also ensures that no other distutils extension monkeypatched the distutils
    first.
    """
    external_bases = (
        cast(type[_T], cls)
        for cls in _get_mro(cls)
        if not cls.__module__.startswith('setuptools')
    )
    base = next(external_bases)
    if not base.__module__.startswith('distutils'):
        msg = f"distutils has already been patched by {cls!r}"
        raise AssertionError(msg)
    return base

