
def _definition_equivalent_to_call(
    definition: _ParameterSignature, call: _CallSignature
) -> bool:
    """Check if a definition signature is equivalent to a call."""
    if definition.kwargs:
        if definition.kwargs not in call.starred_kws:
            return False
    elif call.starred_kws:
        return False
    if definition.varargs:
        if definition.varargs not in call.starred_args:
            return False
    elif call.starred_args:
        return False
    if any(kw not in call.kws for kw in definition.kwonlyargs):
        return False
    if definition.args != call.args:
        return False

    # No extra kwargs in call.
    return all(kw in call.args or kw in definition.kwonlyargs for kw in call.kws)

