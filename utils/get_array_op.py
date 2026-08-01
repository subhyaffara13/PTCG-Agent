
def get_array_op(op):
    """
    Return a binary array operation corresponding to the given operator op.

    Parameters
    ----------
    op : function
        Binary operator from operator or roperator module.

    Returns
    -------
    functools.partial
    """
    if isinstance(op, partial):
        # We get here via dispatch_to_series in DataFrame case
        # e.g. test_rolling_consistency_var_debiasing_factors
        return op

    op_name = op.__name__.strip("_").lstrip("r")
    if op_name == "arith_op":
        # Reached via DataFrame._combine_frame i.e. flex methods
        # e.g. test_df_add_flex_filled_mixed_dtypes
        return op

    if op_name in {"eq", "ne", "lt", "le", "gt", "ge"}:
        return partial(comparison_op, op=op)
    elif op_name in {"and", "or", "xor", "rand", "ror", "rxor"}:
        return partial(logical_op, op=op)
    elif op_name in {
        "add",
        "sub",
        "mul",
        "truediv",
        "floordiv",
        "mod",
        "divmod",
        "pow",
    }:
        return partial(arithmetic_op, op=op)
    else:
        raise NotImplementedError(op_name)

