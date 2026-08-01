
def test_array_equivalent_nested_dicts(strict_nan):
    left = np.array([{"f1": 1, "f2": np.array(["a", "b"], dtype=object)}], dtype=object)
    right = np.array(
        [{"f1": 1, "f2": np.array(["a", "b"], dtype=object)}], dtype=object
    )
    assert array_equivalent(left, right, strict_nan=strict_nan)
    assert not array_equivalent(left, right[::-1], strict_nan=strict_nan)

    right2 = np.array([{"f1": 1, "f2": ["a", "b"]}], dtype=object)
    assert array_equivalent(left, right2, strict_nan=strict_nan)
    assert not array_equivalent(left, right2[::-1], strict_nan=strict_nan)

