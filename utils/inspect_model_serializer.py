
def inspect_model_serializer(serializer: Callable[..., Any], mode: Literal['plain', 'wrap']) -> bool:
    """Look at a model serializer function and determine whether it takes an info argument.

    An error is raised if the function has an invalid signature.

    Args:
        serializer: The serializer function to check.
        mode: The serializer mode, either 'plain' or 'wrap'.

    Returns:
        `info_arg` - whether the function expects an info argument.
    """
    if isinstance(serializer, (staticmethod, classmethod)) or not is_instance_method_from_sig(serializer):
        raise PydanticUserError(
            '`@model_serializer` must be applied to instance methods', code='model-serializer-instance-method'
        )

    sig = signature_no_eval(serializer)
    info_arg = _serializer_info_arg(mode, count_positional_required_params(sig))
    if info_arg is None:
        raise PydanticUserError(
            f'Unrecognized model_serializer function signature for {serializer} with `mode={mode}`:{sig}',
            code='model-serializer-signature',
        )
    else:
        return info_arg

