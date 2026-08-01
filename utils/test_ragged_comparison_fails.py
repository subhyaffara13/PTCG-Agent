
def test_ragged_comparison_fails(op):
    # This needs to convert the internal array to True/False, which fails:
    a = np.array([1, np.array([1, 2, 3])], dtype=object)
    b = np.array([1, np.array([1, 2, 3])], dtype=object)

    with pytest.raises(ValueError, match="The truth value.*ambiguous"):
        op(a, b)

