
def test_array_equivalent_nested_mixed_list(strict_nan):
    # mixed arrays / lists in left and right
    # https://github.com/pandas-dev/pandas/issues/50360
    left = np.array([np.array([1, 2, 3]), np.array([4, 5])], dtype=object)
    right = np.array([[1, 2, 3], [4, 5]], dtype=object)

    assert array_equivalent(left, right, strict_nan=strict_nan)
    assert not array_equivalent(left, right[::-1], strict_nan=strict_nan)

    # multiple levels of nesting
    left = np.array(
        [
            np.array([np.array([1, 2, 3]), np.array([4, 5])], dtype=object),
            np.array([np.array([6]), np.array([7, 8]), np.array([9])], dtype=object),
        ],
        dtype=object,
    )
    right = np.array([[[1, 2, 3], [4, 5]], [[6], [7, 8], [9]]], dtype=object)
    assert array_equivalent(left, right, strict_nan=strict_nan)
    assert not array_equivalent(left, right[::-1], strict_nan=strict_nan)

    # same-length lists
    subarr = np.empty(2, dtype=object)
    subarr[:] = [
        np.array([None, "b"], dtype=object),
        np.array(["c", "d"], dtype=object),
    ]
    left = np.array([subarr, None], dtype=object)
    right = np.array([[[None, "b"], ["c", "d"]], None], dtype=object)
    assert array_equivalent(left, right, strict_nan=strict_nan)
    assert not array_equivalent(left, right[::-1], strict_nan=strict_nan)

