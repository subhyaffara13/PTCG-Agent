
def test_mismatched_length_cmp_op(cons):
    left = SparseArray([True, True])
    right = cons([True, True, True])
    with pytest.raises(ValueError, match="operands have mismatched length"):
        left & right

