
def test_diags_int_to_float64(func):
    d = [[3], [1, 2], [4]]
    offsets = [-1, 0, 1]
    # Until the deprecation period is over, diags and diag_array will cast
    # integer inputs to float64 by default.  A warning will be generated
    # that indicates this behavior is deprecated.
    # See gh-23102.
    with pytest.warns(FutureWarning, match="output has been cast to"):
        arr = func(d, offsets=offsets)
    expected = np.array([[1.0, 4.0], [3.0, 2.0]])
    assert_array_equal(arr.toarray(), expected, strict=True)

