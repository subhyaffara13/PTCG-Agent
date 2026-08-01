
def _add_eq(cls, attrs=None):
    """
    Add equality methods to *cls* with *attrs*.
    """
    if attrs is None:
        attrs = cls.__attrs_attrs__

    script, globs = _make_eq_script(attrs)
    _compile_and_eval(
        script, globs, filename=_generate_unique_filename(cls, "__eq__")
    )
    cls.__eq__ = globs["__eq__"]
    cls.__ne__ = __ne__

    return cls

