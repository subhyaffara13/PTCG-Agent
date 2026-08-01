
def _bool_arith_fallback(op_str, left_op, right_op) -> bool:
    """
    Check if we should fallback to the python `_evaluate_standard` in case
    of an unsupported operation by numexpr, which is the case for some
    boolean ops.
    """
    if _has_bool_dtype(left_op) and _has_bool_dtype(right_op):
        if op_str in _BOOL_OP_UNSUPPORTED:
            warnings.warn(
                f"evaluating in Python space because the {op_str!r} "
                "operator is not supported by numexpr for the bool dtype, "
                f"use {_BOOL_OP_UNSUPPORTED[op_str]!r} instead.",
                stacklevel=find_stack_level(),
            )
            return True
    return False

