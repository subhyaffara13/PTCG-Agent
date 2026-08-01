
def test_array_equivalent_array_mismatched_dtype():
    # same shape, different dtype can still be equivalent
    first = np.array([1, 2], dtype=np.float64)
    second = np.array([1, 2])

    left = Series([first, "a"], dtype=object)
    right = Series([second, "a"], dtype=object)
    assert array_equivalent(left, right)

