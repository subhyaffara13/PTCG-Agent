import itertools

def group_functions_by_op_name(
    grouped_native_functions: Sequence[NativeGroupT],
) -> Sequence[Sequence[NativeGroupT]]:
    if not grouped_native_functions:
        return []
    groups = []

    def is_supported(g: NativeFunctionsGroup | NativeFunctionsViewGroup) -> bool:
        with native_function_manager(g):
            return generator.is_supported(g)

    eligible_ops = (g for g in grouped_native_functions if is_supported(g))
    groups = [
        list(group)
        for k, group in (
            itertools.groupby(
                eligible_ops,
                key=config.func_name_base_str,
            )
        )
    ]

    return groups

