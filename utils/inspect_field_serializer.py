from typing import Any, Callable

def inspect_field_serializer(serializer: Callable[..., Any], mode: Literal['plain', 'wrap']) -> tuple[bool, bool]:
    """Look at a field serializer function and determine if it is a field serializer,
    and whether it takes an info argument.

    An error is raised if the function has an invalid signature.

    Args:
        serializer: The serializer function to inspect.
        mode: The serializer mode, either 'plain' or 'wrap'.

    Returns:
        Tuple of (is_field_serializer, info_arg).
    """
    try:
        sig = signature_no_eval(serializer)
    except (ValueError, TypeError):
        # `inspect.signature` might not be able to infer a signature, e.g. with C objects.
        # In this case, we assume no info argument is present and this is not a method:
        return (False, False)

    first = next(iter(sig.parameters.values()), None)
    is_field_serializer = first is not None and first.name == 'self'

    n_positional = count_positional_required_params(sig)
    if is_field_serializer:
        # -1 to correct for self parameter
        info_arg = _serializer_info_arg(mode, n_positional - 1)
    else:
        info_arg = _serializer_info_arg(mode, n_positional)

    if info_arg is None:
        raise PydanticUserError(
            f'Unrecognized field_serializer function signature for {serializer} with `mode={mode}`:{sig}',
            code='field-serializer-signature',
        )

    return is_field_serializer, info_arg

