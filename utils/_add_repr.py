
def _add_repr(cls, ns=None, attrs=None):
    """
    Add a repr method to *cls*.
    """
    if attrs is None:
        attrs = cls.__attrs_attrs__

    script, globs = _make_repr_script(attrs, ns)
    _compile_and_eval(
        script, globs, filename=_generate_unique_filename(cls, "__repr__")
    )
    cls.__repr__ = globs["__repr__"]
    return cls

