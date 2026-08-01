
def test_select_step24(args, kwargs, expected_levels, expected_factor):
    levels, n, factor = select_step24(*args, **kwargs)

    assert n == len(levels)
    np.testing.assert_array_equal(levels, expected_levels)
    assert factor == expected_factor

