
def consider_sys_version_info(expr: Expression, pyversion: tuple[int, ...]) -> int:
    """Consider whether expr is a comparison involving sys.version_info.

    Return ALWAYS_TRUE, ALWAYS_FALSE, or TRUTH_VALUE_UNKNOWN.
    """
    # Cases supported:
    # - sys.version_info[<int>] <compare_op> <int>
    # - sys.version_info[:<int>] <compare_op> <tuple_of_n_ints>
    # - sys.version_info <compare_op> <tuple_of_1_or_2_ints>
    #   (in this case <compare_op> must be >, >=, <, <=, but cannot be ==, !=)
    if not isinstance(expr, ComparisonExpr):
        return TRUTH_VALUE_UNKNOWN
    # Let's not yet support chained comparisons.
    if len(expr.operators) > 1:
        return TRUTH_VALUE_UNKNOWN
    op = expr.operators[0]
    if op not in ("==", "!=", "<=", ">=", "<", ">"):
        return TRUTH_VALUE_UNKNOWN

    index = contains_sys_version_info(expr.operands[0])
    thing = contains_int_or_tuple_of_ints(expr.operands[1])
    if index is None or thing is None:
        index = contains_sys_version_info(expr.operands[1])
        thing = contains_int_or_tuple_of_ints(expr.operands[0])
        op = reverse_op[op]
    if isinstance(index, int) and isinstance(thing, int):
        # sys.version_info[i] <compare_op> k
        if 0 <= index <= 1:
            return fixed_comparison(pyversion[index], op, thing)
        else:
            return TRUTH_VALUE_UNKNOWN
    elif isinstance(index, tuple) and isinstance(thing, tuple):
        lo, hi = index
        if lo is None:
            lo = 0
        if hi is None:
            hi = 2
        if 0 <= lo < hi <= 2:
            val = pyversion[lo:hi]
            if len(val) == len(thing) or len(val) > len(thing) and op not in ("==", "!="):
                return fixed_comparison(val, op, thing)
    return TRUTH_VALUE_UNKNOWN

