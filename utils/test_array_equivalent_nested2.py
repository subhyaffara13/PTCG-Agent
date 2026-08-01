
def test_array_equivalent_nested2(strict_nan):
    # more than one level of nesting
    left = np.array(
        [
            np.array([np.array([50, 70]), np.array([90])], dtype=object),
            np.array([np.array([20, 30])], dtype=object),
        ],
        dtype=object,
    )
    right = np.array(
        [
            np.array([np.array([50, 70]), np.array([90])], dtype=object),
            np.array([np.array([20, 30])], dtype=object),
        ],
        dtype=object,
    )
    assert array_equivalent(left, right, strict_nan=strict_nan)
    assert not array_equivalent(left, right[::-1], strict_nan=strict_nan)

    left = np.array([np.array([np.array([50, 50, 50])], dtype=object)], dtype=object)
    right = np.array([50])
    assert not array_equivalent(left, right, strict_nan=strict_nan)

