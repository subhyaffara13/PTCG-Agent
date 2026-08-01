
def iter_field_objects(fields: _TYPE_FIELDS) -> typing.Iterable[RequestField]:
    """
    Iterate over fields.

    Supports list of (k, v) tuples and dicts, and lists of
    :class:`~urllib3.fields.RequestField`.

    """
    iterable: typing.Iterable[RequestField | tuple[str, _TYPE_FIELD_VALUE_TUPLE]]

    if isinstance(fields, typing.Mapping):
        iterable = fields.items()
    else:
        iterable = fields

    for field in iterable:
        if isinstance(field, RequestField):
            yield field
        else:
            yield RequestField.from_tuples(*field)


def iter_field_objects(fields: _TYPE_FIELDS) -> typing.Iterable[RequestField]:
    """
    Iterate over fields.

    Supports list of (k, v) tuples and dicts, and lists of
    :class:`~urllib3.fields.RequestField`.

    """
    iterable: typing.Iterable[RequestField | tuple[str, _TYPE_FIELD_VALUE_TUPLE]]

    if isinstance(fields, typing.Mapping):
        iterable = fields.items()
    else:
        iterable = fields

    for field in iterable:
        if isinstance(field, RequestField):
            yield field
        else:
            yield RequestField.from_tuples(*field)

