
def _has_different_parameters_default_value(
    original: nodes.Arguments, overridden: nodes.Arguments
) -> bool:
    """Check if original and overridden methods arguments have different default values.

    Return True if one of the overridden arguments has a default
    value different from the default value of the original argument
    If one of the method doesn't have argument (.args is None)
    return False
    """
    if original.args is None or overridden.args is None:
        return False

    for param in chain(original.args, original.kwonlyargs):
        try:
            original_default = original.default_value(param.name)
        except astroid.exceptions.NoDefault:
            original_default = _DEFAULT_MISSING
        try:
            overridden_default = overridden.default_value(param.name)
            if original_default is _DEFAULT_MISSING:
                # Only the original has a default.
                return True
        except astroid.exceptions.NoDefault:
            if original_default is _DEFAULT_MISSING:
                # Both have a default, no difference
                continue
            # Only the override has a default.
            return True

        original_type = type(original_default)
        if not isinstance(overridden_default, original_type):
            # Two args with same name but different types
            return True
        is_same_fn: Callable[[Any, Any], bool] | None = ASTROID_TYPE_COMPARATORS.get(
            original_type
        )
        if is_same_fn is None:
            # If the default value comparison is unhandled, assume the value is different
            return True
        if not is_same_fn(original_default, overridden_default):
            # Two args with same type but different values
            return True
    return False

