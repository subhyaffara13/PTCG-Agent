
def test_integer_comparison_with_cast(arr):
    # Similar to above, but mainly test a few cases that cover the slow path
    # the test is limited to unsigned ints and -1 for simplicity.
    res = arr >= -1
    assert_array_equal(res, np.ones_like(arr, dtype=bool))
    res = arr < -1
    assert_array_equal(res, np.zeros_like(arr, dtype=bool))

