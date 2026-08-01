
def _get_init_params(cls: Type) -> frozenset:
    """Extract parameter names from a class's __init__ method."""
    sig = inspect.signature(cls.__init__)
    return frozenset(
        name
        for name, param in sig.parameters.items()
        if name != "self"
        and param.kind
        in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        )
    )

