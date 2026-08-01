
def deep_iterable(member_validator, iterable_validator=None):
    """
    A validator that performs deep validation of an iterable.

    Args:
        member_validator: Validator(s) to apply to iterable members.

        iterable_validator:
            Validator(s) to apply to iterable itself (optional).

    Raises
        TypeError: if any sub-validators fail

    .. versionadded:: 19.1.0

    .. versionchanged:: 25.4.0
       *member_validator* and *iterable_validator* can now be a list or tuple
       of validators.
    """
    if isinstance(member_validator, (list, tuple)):
        member_validator = and_(*member_validator)
    if isinstance(iterable_validator, (list, tuple)):
        iterable_validator = and_(*iterable_validator)
    return _DeepIterable(member_validator, iterable_validator)

