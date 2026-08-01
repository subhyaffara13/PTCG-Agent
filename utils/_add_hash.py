
def _add_hash(cls: type, attrs: list[Attribute]):
    """
    Add a hash method to *cls*.
    """
    script, globs = _make_hash_script(
        cls, attrs, frozen=False, cache_hash=False
    )
    _compile_and_eval(
        script, globs, filename=_generate_unique_filename(cls, "__hash__")
    )
    cls.__hash__ = globs["__hash__"]
    return cls

