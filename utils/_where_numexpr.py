
def _where_numexpr(cond, left_op, right_op):
    # Caller is responsible for extracting ndarray if necessary
    result = None

    if _can_use_numexpr(None, "where", left_op, right_op, "where"):
        result = ne.evaluate(
            "where(cond_value, a_value, b_value)",
            local_dict={"cond_value": cond, "a_value": left_op, "b_value": right_op},
            casting="safe",
        )

    if result is None:
        result = _where_standard(cond, left_op, right_op)

    return result

