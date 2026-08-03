from typing import Any

def sequence_validator(
    input_value: Sequence[Any],
    /,
    validator: core_schema.ValidatorFunctionWrapHandler,
) -> Sequence[Any]:
    """Validator for `Sequence` types, isinstance(v, Sequence) has already been called."""
    value_type = type(input_value)

    # We don't accept any plain string as a sequence
    # Relevant issue: https://github.com/pydantic/pydantic/issues/5595
    if issubclass(value_type, (str, bytes)):
        raise PydanticCustomError(
            'sequence_str',
            "'{type_name}' instances are not allowed as a Sequence value",
            {'type_name': value_type.__name__},
        )

    # TODO: refactor sequence validation to validate with either a list or a tuple
    # schema, depending on the type of the value.
    # Additionally, we should be able to remove one of either this validator or the
    # SequenceValidator in _std_types_schema.py (preferably this one, while porting over some logic).
    # Effectively, a refactor for sequence validation is needed.
    if value_type is tuple:
        input_value = list(input_value)

    v_list = validator(input_value)

    # the rest of the logic is just re-creating the original type from `v_list`
    if value_type is list:
        return v_list
    elif issubclass(value_type, range):
        # return the list as we probably can't re-create the range
        return v_list
    elif value_type is tuple:
        return tuple(v_list)
    else:
        # best guess at how to re-create the original type, more custom construction logic might be required
        return value_type(v_list)  # type: ignore[call-arg]

