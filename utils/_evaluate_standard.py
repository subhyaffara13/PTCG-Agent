
def _evaluate_standard(op, op_str, left_op, right_op):
    """
    Standard evaluation.
    """
    if _TEST_MODE:
        _store_test_result(False)
    return op(left_op, right_op)

