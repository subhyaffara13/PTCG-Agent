
def _signature_metadata(
    sig: inspect.Signature,
) -> tuple[tuple[inspect.Parameter, ...], bool, int]:
    """
    Returns tuple(sig.parameters.values()), if any has VAR_POSITIONAL or VAR_KEYWORD, and the max_positional
    """
    params = tuple(sig.parameters.values())
    has_var_args = False
    max_positional = 0

    for p in params:
        kind = p.kind
        if kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            has_var_args = True
        if kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            max_positional += 1

    return params, has_var_args, max_positional

