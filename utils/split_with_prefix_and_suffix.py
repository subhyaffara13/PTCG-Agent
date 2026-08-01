
def split_with_prefix_and_suffix(
    types: tuple[Type, ...], prefix: int, suffix: int
) -> tuple[tuple[Type, ...], tuple[Type, ...], tuple[Type, ...]]:
    if len(types) <= prefix + suffix:
        types = extend_args_for_prefix_and_suffix(types, prefix, suffix)
    if suffix:
        return types[:prefix], types[prefix:-suffix], types[-suffix:]
    else:
        return types[:prefix], types[prefix:], ()

