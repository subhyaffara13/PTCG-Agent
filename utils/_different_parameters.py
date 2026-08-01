
def _different_parameters(
    original: nodes.FunctionDef,
    overridden: nodes.FunctionDef,
    dummy_parameter_regex: Pattern[str],
) -> list[str]:
    """Determine if the two methods have different parameters.

    They are considered to have different parameters if:

       * they have different positional parameters, including different names

       * one of the methods is having variadics, while the other is not

       * they have different keyword only parameters.
    """
    output_messages = []
    original_parameters = _positional_parameters(original)
    overridden_parameters = _positional_parameters(overridden)

    # Copy kwonlyargs list so that we don't affect later function linting
    original_kwonlyargs = original.args.kwonlyargs

    # Allow positional/keyword variadic in overridden to match against any
    # positional/keyword argument in original.
    # Keep any arguments that are found separately in overridden to satisfy
    # later tests
    if overridden.args.vararg:
        overridden_names = [v.name for v in overridden_parameters]
        original_parameters = [
            v for v in original_parameters if v.name in overridden_names
        ]

    if overridden.args.kwarg:
        overridden_names = [v.name for v in overridden.args.kwonlyargs]
        original_kwonlyargs = [
            v for v in original.args.kwonlyargs if v.name in overridden_names
        ]

    different_positional = _has_different_parameters(
        original_parameters, overridden_parameters, dummy_parameter_regex
    )
    different_kwonly = _has_different_keyword_only_parameters(
        original_kwonlyargs, overridden.args.kwonlyargs
    )
    if different_kwonly and different_positional:
        if "Number " in different_positional[0] and "Number " in different_kwonly[0]:
            output_messages.append("Number of parameters ")
            output_messages += different_positional[1:]
            output_messages += different_kwonly[1:]
        else:
            output_messages += different_positional
            output_messages += different_kwonly
    else:
        if different_positional:
            output_messages += different_positional
        if different_kwonly:
            output_messages += different_kwonly

    # Arguments will only violate LSP if there are variadics in the original
    # that are then removed from the overridden
    kwarg_lost = original.args.kwarg and not overridden.args.kwarg
    vararg_lost = original.args.vararg and not overridden.args.vararg

    if kwarg_lost or vararg_lost:
        output_messages += ["Variadics removed in"]

    if original.name in PYMETHODS:
        # Ignore the difference for special methods. If the parameter
        # numbers are different, then that is going to be caught by
        # unexpected-special-method-signature.
        # If the names are different, it doesn't matter, since they can't
        # be used as keyword arguments anyway.
        output_messages.clear()

    return output_messages

