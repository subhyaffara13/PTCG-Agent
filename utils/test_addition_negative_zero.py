
def test_addition_negative_zero(dtype):
    dtype = np.dtype(dtype)
    if dtype.kind == "c":
        neg_zero = dtype.type(complex(-0.0, -0.0))
    else:
        neg_zero = dtype.type(-0.0)

    arr = np.array(neg_zero)
    arr2 = np.array(neg_zero)

    assert _check_neg_zero(arr + arr2)
    # In-place ops may end up on a different path (reduce path) see gh-21211
    arr += arr2
    assert _check_neg_zero(arr)

