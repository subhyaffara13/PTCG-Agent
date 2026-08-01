
def include(*what):
    """
    Create a filter that only allows *what*.

    Args:
        what (list[type, str, attrs.Attribute]):
            What to include. Can be a type, a name, or an attribute.

    Returns:
        Callable:
            A callable that can be passed to `attrs.asdict`'s and
            `attrs.astuple`'s *filter* argument.

    .. versionchanged:: 23.1.0 Accept strings with field names.
    """
    cls, names, attrs = _split_what(what)

    def include_(attribute, value):
        return (
            value.__class__ in cls
            or attribute.name in names
            or attribute in attrs
        )

    return include_

