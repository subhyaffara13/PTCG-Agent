
def count_positional_required_params(sig: Signature) -> int:
    """Get the number of positional (required) arguments of a signature.

    This function should only be used to inspect signatures of validation and serialization functions.
    The first argument (the value being serialized or validated) is counted as a required argument
    even if a default value exists.

    Returns:
        The number of positional arguments of a signature.
    """
    parameters = list(sig.parameters.values())
    return sum(
        1
        for param in parameters
        if can_be_positional(param)
        # First argument is the value being validated/serialized, and can have a default value
        # (e.g. `float`, which has signature `(x=0, /)`). We assume other parameters (the info arg
        # for instance) should be required, and thus without any default value.
        and (param.default is Parameter.empty or param is parameters[0])
    )

