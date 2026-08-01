
def getfuncargnames(
    function: Callable[..., object],
    *,
    name: str = "",
    cls: type | None = None,
) -> tuple[str, ...]:
    """Return the names of a function's mandatory arguments.

    Should return the names of all function arguments that:
    * Aren't bound to an instance or type as in instance or class methods.
    * Don't have default values.
    * Aren't bound with functools.partial.
    * Aren't replaced with mocks.

    The cls arguments indicate that the function should be treated as a bound
    method even though it's not unless the function is a static method.

    The name parameter should be the original name in which the function was collected.
    """
    # TODO(RonnyPfannschmidt): This function should be refactored when we
    # revisit fixtures. The fixture mechanism should ask the node for
    # the fixture names, and not try to obtain directly from the
    # function object well after collection has occurred.

    # The parameters attribute of a Signature object contains an
    # ordered mapping of parameter names to Parameter instances.  This
    # creates a tuple of the names of the parameters that don't have
    # defaults.
    try:
        parameters = signature(function).parameters.values()
    except (ValueError, TypeError) as e:
        from _pytest.outcomes import fail

        fail(
            f"Could not determine arguments of {function!r}: {e}",
            pytrace=False,
        )

    arg_names = tuple(
        p.name
        for p in parameters
        if (
            p.kind is Parameter.POSITIONAL_OR_KEYWORD
            or p.kind is Parameter.KEYWORD_ONLY
        )
        and p.default is Parameter.empty
    )
    if not name:
        name = function.__name__

    # If this function should be treated as a bound method even though
    # it's passed as an unbound method or function, and its first parameter
    # wasn't defined as positional only, remove the first parameter name.
    if not any(p.kind is Parameter.POSITIONAL_ONLY for p in parameters) and (
        # Not using `getattr` because we don't want to resolve the staticmethod.
        # Not using `cls.__dict__` because we want to check the entire MRO.
        cls
        and not isinstance(
            inspect.getattr_static(cls, name, default=None), staticmethod
        )
    ):
        arg_names = arg_names[1:]
    # Remove any names that will be replaced with mocks.
    if hasattr(function, "__wrapped__"):
        arg_names = arg_names[num_mock_patch_args(function) :]
    return arg_names

