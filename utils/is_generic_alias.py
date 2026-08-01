
def is_generic_alias(tp: Any, /) -> bool:
    return isinstance(tp, (types.GenericAlias, typing._GenericAlias))  # pyright: ignore[reportAttributeAccessIssue]

