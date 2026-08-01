
def _class_reduce(obj):
    """Select the reducer depending on the dynamic nature of the class obj."""
    if obj is type(None):  # noqa
        return type, (None,)
    elif obj is type(Ellipsis):
        return type, (Ellipsis,)
    elif obj is type(NotImplemented):
        return type, (NotImplemented,)
    elif obj in _BUILTIN_TYPE_NAMES:
        return _builtin_type, (_BUILTIN_TYPE_NAMES[obj],)
    elif not _should_pickle_by_reference(obj):
        return _dynamic_class_reduce(obj)
    return NotImplemented

