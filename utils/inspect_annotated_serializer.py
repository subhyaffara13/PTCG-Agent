
def inspect_annotated_serializer(serializer: Callable[..., Any], mode: Literal['plain', 'wrap']) -> bool:
    """Look at a serializer function used via `Annotated` and determine whether it takes an info argument.

    An error is raised if the function has an invalid signature.

    Args:
        serializer: The serializer function to check.
        mode: The serializer mode, either 'plain' or 'wrap'.

    Returns:
        info_arg
    """
    try:
        sig = signature_no_eval(serializer)
    except (ValueError, TypeError):
        # `inspect.signature` might not be able to infer a signature, e.g. with C objects.
        # In this case, we assume no info argument is present:
        return False
    info_arg = _serializer_info_arg(mode, count_positional_required_params(sig))
    if info_arg is None:
        raise PydanticUserError(
            f'Unrecognized field_serializer function signature for {serializer} with `mode={mode}`:{sig}',
            code='field-serializer-signature',
        )
    else:
        return info_arg

