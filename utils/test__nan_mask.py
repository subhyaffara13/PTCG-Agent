
def test__nan_mask(arr, expected):
    for out in [None, np.empty(arr.shape, dtype=np.bool)]:
        actual = _nan_mask(arr, out=out)
        assert_equal(actual, expected)
        # the above won't distinguish between True proper
        # and an array of True values; we want True proper
        # for types that can't possibly contain NaN
        if type(expected) is not np.ndarray:
            assert actual is True

