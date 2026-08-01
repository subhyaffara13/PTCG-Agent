
def optional(converter):
    """
    A converter that allows an attribute to be optional. An optional attribute
    is one which can be set to `None`.

    Type annotations will be inferred from the wrapped converter's, if it has
    any.

    Args:
        converter (typing.Callable):
            the converter that is used for non-`None` values.

    .. versionadded:: 17.1.0
    """

    if isinstance(converter, Converter):

        def optional_converter(val, inst, field):
            if val is None:
                return None
            return converter(val, inst, field)

    else:

        def optional_converter(val):
            if val is None:
                return None
            return converter(val)

    xtr = _AnnotationExtractor(converter)

    t = xtr.get_first_param_type()
    if t:
        optional_converter.__annotations__["val"] = typing.Optional[t]

    rt = xtr.get_return_type()
    if rt:
        optional_converter.__annotations__["return"] = typing.Optional[rt]

    if isinstance(converter, Converter):
        return Converter(optional_converter, takes_self=True, takes_field=True)

    return optional_converter


def optional(validator):
    """
    A validator that makes an attribute optional.  An optional attribute is one
    which can be set to `None` in addition to satisfying the requirements of
    the sub-validator.

    Args:
        validator
            (typing.Callable | tuple[typing.Callable] | list[typing.Callable]):
            A validator (or validators) that is used for non-`None` values.

    .. versionadded:: 15.1.0
    .. versionchanged:: 17.1.0 *validator* can be a list of validators.
    .. versionchanged:: 23.1.0 *validator* can also be a tuple of validators.
    """
    if isinstance(validator, (list, tuple)):
        return _OptionalValidator(_AndValidator(validator))

    return _OptionalValidator(validator)

