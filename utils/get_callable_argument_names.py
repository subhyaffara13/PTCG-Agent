
def get_callable_argument_names(fn) -> list[str]:
    """
    Gets names of all POSITIONAL_OR_KEYWORD arguments for callable `fn`.
    Returns an empty list when other types of arguments are present.

    This is used by `torch.jit.trace` to assign meaningful argument names to
    traced functions and modules.

    Args:
        fn: A callable.
    Returns:
        Argument names: List[str]
    """
    # inspect.signature may fail, give up in that case.
    try:
        callable_signature = inspect.signature(fn)
    except Exception:
        return []

    argument_names = []
    for name, param in callable_signature.parameters.items():
        # All four other types of arguments do not map to individual values
        # with a keyword as name.
        if param.kind != param.POSITIONAL_OR_KEYWORD:
            continue

        argument_names.append(name)

    return argument_names

