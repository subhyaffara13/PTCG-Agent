
def test_comparison_ops(comparison_op, other):
    assert comparison_op(NA, other) is NA
    assert comparison_op(other, NA) is NA

