
def _check_namedtuple_attributes(typename, attributes, rename=False):
    attributes = tuple(attributes)
    if rename:
        attributes = _get_renamed_namedtuple_attributes(attributes)

    # The following snippet is derived from the CPython Lib/collections/__init__.py sources
    # <snippet>
    for name in (typename, *attributes):
        if not isinstance(name, str):
            raise AstroidTypeError(
                f"Type names and field names must be strings, not {type(name)!r}"
            )
        if not name.isidentifier():
            raise AstroidValueError(
                "Type names and field names must be valid" + f"identifiers: {name!r}"
            )
        if keyword.iskeyword(name):
            raise AstroidValueError(
                f"Type names and field names cannot be a keyword: {name!r}"
            )

    seen = set()
    for name in attributes:
        if name.startswith("_") and not rename:
            raise AstroidValueError(
                f"Field names cannot start with an underscore: {name!r}"
            )
        if name in seen:
            raise AstroidValueError(f"Encountered duplicate field name: {name!r}")
        seen.add(name)
    # </snippet>

    return attributes

