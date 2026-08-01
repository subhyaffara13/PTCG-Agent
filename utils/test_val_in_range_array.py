
def test_val_in_range_array():
    # Vectorized: scalar in -> scalar bool, array in -> bool array.
    arr = np.array([0.5, -1.0, 0.0, np.nan, np.inf, 0.25])
    cases = {
        'linear': [True, True, True, False, False, True],
        'log':    [True, False, False, False, False, True],
        'symlog': [True, True, True, False, False, True],
        'asinh':  [True, True, True, False, False, True],
        'logit':  [True, False, False, False, False, True],
    }
    for name, expected in cases.items():
        s = mscale._scale_mapping[name](axis=None)
        np.testing.assert_array_equal(s.val_in_range(arr), expected)

    # 2D shape is preserved.
    out = mscale._scale_mapping['log'](axis=None).val_in_range(
        np.array([[1.0, -1.0], [0.5, np.nan]]))
    np.testing.assert_array_equal(out, [[True, False], [True, False]])

