
def _evaluate_numexpr(op, op_str, left_op, right_op):
    result = None

    if _can_use_numexpr(op, op_str, left_op, right_op, "evaluate"):
        is_reversed = op.__name__.strip("_").startswith("r")
        if is_reversed:
            # we were originally called by a reversed op method
            left_op, right_op = right_op, left_op

        left_value = left_op
        right_value = right_op

        try:
            result = ne.evaluate(
                f"left_value {op_str} right_value",
                local_dict={"left_value": left_value, "right_value": right_value},
                casting="safe",
            )
        except TypeError:
            # numexpr raises eg for array ** array with integers
            # (https://github.com/pydata/numexpr/issues/379)
            pass
        except NotImplementedError:
            if _bool_arith_fallback(op_str, left_op, right_op):
                pass
            else:
                raise

        if is_reversed:
            # reverse order to original for fallback
            left_op, right_op = right_op, left_op

    if _TEST_MODE:
        _store_test_result(result is not None)

    if result is None:
        result = _evaluate_standard(op, op_str, left_op, right_op)

    return result

