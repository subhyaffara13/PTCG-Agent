
def _binary_search_insert_arg(
    ordered_args: list[sympy.Basic], new_arg: sympy.Basic
) -> list[sympy.Basic] | None:
    """
    If new_arg is found in ordered_args None is returned, else the new
    ordered_args with new_arg inserted
    """
    if len(ordered_args) == 0:
        return [new_arg]

    from sympy.core.basic import _args_sortkey as sort_key, Basic

    # Fast path when new_arg > ordered_args[-1].
    if sort_key(ordered_args[-1]) < sort_key(new_arg):
        return ordered_args + [new_arg]

    # Fast path when new_arg < ordered_args[0].
    if sort_key(ordered_args[0]) > sort_key(new_arg):
        return [new_arg] + ordered_args

    low, high = 0, len(ordered_args) - 1

    while low <= high:
        mid = (low + high) // 2
        compare_result = Basic.compare(ordered_args[mid], new_arg)
        if compare_result == 0:
            return None
        elif compare_result < 0:
            low = mid + 1
        else:
            high = mid - 1

    ordered_args.insert(low, new_arg)
    return ordered_args

