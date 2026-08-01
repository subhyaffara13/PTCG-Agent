
def test_array_equivalent_nested_list(strict_nan):
    left = np.array([[50, 70, 90], [20, 30]], dtype=object)
    right = np.array([[50, 70, 90], [20, 30]], dtype=object)

    assert array_equivalent(left, right, strict_nan=strict_nan)
    assert not array_equivalent(left, right[::-1], strict_nan=strict_nan)

    left = np.array([[50, 50, 50], [40, 40]], dtype=object)
    right = np.array([50, 40])
    assert not array_equivalent(left, right, strict_nan=strict_nan)

