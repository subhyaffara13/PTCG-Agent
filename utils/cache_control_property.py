
def cache_control_property(
    key: str, empty: t.Any, type: type[t.Any] | None, *, doc: str | None = None
) -> t.Any:
    """Return a new property object for a cache header. Useful if you
    want to add support for a cache extension in a subclass.

    :param key: The attribute name present in the parsed cache-control header dict.
    :param empty: The value to use if the key is present without a value.
    :param type: The type to convert the string value to instead of a string. If
        conversion raises a ``ValueError``, the returned value is ``None``.
    :param doc: The docstring for the property. If not given, it is generated
        based on the other params.

    .. versionchanged:: 3.1
        Added the ``doc`` param.

    .. versionchanged:: 2.0
        Renamed from ``cache_property``.
    """
    if doc is None:
        parts = [f"The ``{key}`` attribute."]

        if type is bool:
            parts.append("A ``bool``, either present or not.")
        else:
            if type is None:
                parts.append("A ``str``,")
            else:
                parts.append(f"A ``{type.__name__}``,")

            if empty is not None:
                parts.append(f"``{empty!r}`` if present with no value,")

            parts.append("or ``None`` if not present.")

        doc = " ".join(parts)

    return property(
        lambda x: x._get_cache_value(key, empty, type),
        lambda x, v: x._set_cache_value(key, v, type),
        lambda x: x._del_cache_value(key),
        doc=cleandoc(doc),
    )

