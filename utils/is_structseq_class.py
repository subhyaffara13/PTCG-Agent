
def is_structseq_class(cls: type) -> bool:
    """Return whether the class is a class of PyStructSequence."""
    return (
        isinstance(cls, type)
        # Check direct inheritance from `tuple` rather than `issubclass(cls, tuple)`
        and cls.__bases__ == (tuple,)
        # Check PyStructSequence members
        and isinstance(getattr(cls, "n_fields", None), int)
        and isinstance(getattr(cls, "n_sequence_fields", None), int)
        and isinstance(getattr(cls, "n_unnamed_fields", None), int)
        # Check the type does not allow subclassing
        and not bool(cls.__flags__ & Py_TPFLAGS_BASETYPE)  # only works for CPython
    )

