
def _is_validator(validator: Any) -> bool:
    """Check if a function is a validator.

    A validator is a Callable that can be called with a single positional argument.
    The validator can have more arguments with default values.

    Basically, returns True if `validator(value)` is possible.
    """
    if not callable(validator):
        return False

    signature = inspect.signature(validator)
    parameters = list(signature.parameters.values())
    if len(parameters) == 0:
        return False
    if parameters[0].kind not in (
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
        inspect.Parameter.POSITIONAL_ONLY,
        inspect.Parameter.VAR_POSITIONAL,
    ):
        return False
    for parameter in parameters[1:]:
        if parameter.default == inspect.Parameter.empty:
            return False
    return True

