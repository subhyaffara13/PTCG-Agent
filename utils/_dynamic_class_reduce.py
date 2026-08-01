
def _dynamic_class_reduce(obj):
    """Save a class that can't be referenced as a module attribute.

    This method is used to serialize classes that are defined inside
    functions, or that otherwise can't be serialized as attribute lookups
    from importable modules.
    """
    if Enum is not None and issubclass(obj, Enum):
        return (
            _make_skeleton_enum,
            _enum_getnewargs(obj),
            _enum_getstate(obj),
            None,
            None,
            _class_setstate,
        )
    else:
        return (
            _make_skeleton_class,
            _class_getnewargs(obj),
            _class_getstate(obj),
            None,
            None,
            _class_setstate,
        )

