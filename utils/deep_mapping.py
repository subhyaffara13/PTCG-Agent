
def deep_mapping(
    key_validator=None, value_validator=None, mapping_validator=None
):
    """
    A validator that performs deep validation of a dictionary.

    All validators are optional, but at least one of *key_validator* or
    *value_validator* must be provided.

    Args:
        key_validator: Validator(s) to apply to dictionary keys.

        value_validator: Validator(s) to apply to dictionary values.

        mapping_validator:
            Validator(s) to apply to top-level mapping attribute.

    .. versionadded:: 19.1.0

    .. versionchanged:: 25.4.0
       *key_validator* and *value_validator* are now optional, but at least one
       of them must be provided.

    .. versionchanged:: 25.4.0
       *key_validator*, *value_validator*, and *mapping_validator* can now be a
       list or tuple of validators.

    Raises:
        TypeError: If any sub-validator fails on validation.

        ValueError:
            If neither *key_validator* nor *value_validator* is provided on
            instantiation.
    """
    if key_validator is None and value_validator is None:
        msg = (
            "At least one of key_validator or value_validator must be provided"
        )
        raise ValueError(msg)

    if isinstance(key_validator, (list, tuple)):
        key_validator = and_(*key_validator)
    if isinstance(value_validator, (list, tuple)):
        value_validator = and_(*value_validator)
    if isinstance(mapping_validator, (list, tuple)):
        mapping_validator = and_(*mapping_validator)

    return _DeepMapping(key_validator, value_validator, mapping_validator)

