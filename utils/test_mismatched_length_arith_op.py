
def test_mismatched_length_arith_op(a, b, all_arithmetic_functions):
    op = all_arithmetic_functions
    with pytest.raises(AssertionError, match=f"length mismatch: {len(a)} vs. {len(b)}"):
        op(SparseArray(a, fill_value=0), np.array(b))

