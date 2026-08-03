from typing import Any, Callable

def inspect_validator(
    validator: Callable[..., Any], *, mode: FieldValidatorModes, type: Literal['field', 'model']
) -> bool:
    """Look at a field or model validator function and determine whether it takes an info argument.

    An error is raised if the function has an invalid signature.

    Args:
        validator: The validator function to inspect.
        mode: The proposed validator mode.
        type: The type of validator, either 'field' or 'model'.

    Returns:
        Whether the validator takes an info argument.
    """
    try:
        sig = signature_no_eval(validator)
    except (ValueError, TypeError):
        # `inspect.signature` might not be able to infer a signature, e.g. with C objects.
        # In this case, we assume no info argument is present:
        return False
    n_positional = count_positional_required_params(sig)
    if mode == 'wrap':
        if n_positional == 3:
            return True
        elif n_positional == 2:
            return False
    else:
        assert mode in {'before', 'after', 'plain'}, f"invalid mode: {mode!r}, expected 'before', 'after' or 'plain"
        if n_positional == 2:
            return True
        elif n_positional == 1:
            return False

    raise PydanticUserError(
        f'Unrecognized {type} validator function signature for {validator} with `mode={mode}`: {sig}',
        code='validator-signature',
    )

