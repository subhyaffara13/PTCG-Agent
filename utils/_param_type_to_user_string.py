
def _param_type_to_user_string(param_type: type[ParameterInfo]) -> str:
    # Render a `ParameterInfo` subclass for use in error messages.
    # User code doesn't call `*Info` directly, so errors should present the classes how
    # they were (probably) defined in the user code.
    if param_type is OptionInfo:
        return "`Option`"
    elif param_type is ArgumentInfo:
        return "`Argument`"
    # This line shouldn't be reachable during normal use.
    return f"`{param_type.__name__}`"  # pragma: no cover

