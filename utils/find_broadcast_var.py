
def find_broadcast_var(
    index: sympy.Expr, var_ranges: dict[sympy.Expr, int]
) -> sympy.Expr | None:
    """
    Try to find the variable that this index is broadcast over.
    A broadcast pattern is one where consecutive values of a variable
    access the same memory location (e.g., x // 10).
    """
    # Approximate analysis by evaluating at 1 and 0
    variables: dict[sympy.Symbol, int] = {}
    for v in index.free_symbols:
        if v in var_ranges:
            variables[v] = 0
        else:
            variables[v] = get_hint(v)

    zero_index = sympy_subs(index, variables)
    for v in var_ranges:
        if v not in index.free_symbols:
            continue

        variables[v] = 1
        try:
            new_val = sympy_subs(index, variables)
        except ZeroDivisionError:
            loop_tiling_log.info("zero division error %s %s", index, variables)
            continue
        # Broadcast means the value doesn't change when the variable increments
        if new_val == zero_index:
            return v
        variables[v] = 0

    return None

