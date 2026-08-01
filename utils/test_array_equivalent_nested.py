
def test_array_equivalent_nested(strict_nan):
    # reached in groupby aggregations, make sure we use np.any when checking
    #  if the comparison is truthy
    left = np.array([np.array([50, 70, 90]), np.array([20, 30])], dtype=object)
    right = np.array([np.array([50, 70, 90]), np.array([20, 30])], dtype=object)

    assert array_equivalent(left, right, strict_nan=strict_nan)
    assert not array_equivalent(left, right[::-1], strict_nan=strict_nan)

    left = np.empty(2, dtype=object)
    left[:] = [np.array([50, 70, 90]), np.array([20, 30, 40])]
    right = np.empty(2, dtype=object)
    right[:] = [np.array([50, 70, 90]), np.array([20, 30, 40])]
    assert array_equivalent(left, right, strict_nan=strict_nan)
    assert not array_equivalent(left, right[::-1], strict_nan=strict_nan)

    left = np.array([np.array([50, 50, 50]), np.array([40, 40])], dtype=object)
    right = np.array([50, 40])
    assert not array_equivalent(left, right, strict_nan=strict_nan)

