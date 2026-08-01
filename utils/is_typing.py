
def is_typing(value: Any) -> bool:
    # _Final catches most of typing classes:
    #   - Any
    #   - Callable
    #   - Union (Python < 3.14)
    #   ...
    #
    # NB: we intentionally ignore classes that inherit from Generic, since they
    # can be used as both TypingVariable as well as UserDefinedClassVariable.
    if sys.version_info >= (3, 12) and isinstance(value, _builtin_final_typing_classes):
        return True
    return (
        isinstance(value, (types.UnionType, typing._Final))  # type: ignore[attr-defined]
        or value is typing.Generic
        or value is typing.Union
    )

