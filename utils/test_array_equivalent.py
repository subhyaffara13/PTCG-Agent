
def test_array_equivalent(dtype_equal):
    assert array_equivalent(
        np.array([np.nan, np.nan]), np.array([np.nan, np.nan]), dtype_equal=dtype_equal
    )
    assert array_equivalent(
        np.array([np.nan, 1, np.nan]),
        np.array([np.nan, 1, np.nan]),
        dtype_equal=dtype_equal,
    )
    assert array_equivalent(
        np.array([np.nan, None], dtype="object"),
        np.array([np.nan, None], dtype="object"),
        dtype_equal=dtype_equal,
    )
    # Check the handling of nested arrays in array_equivalent_object
    assert array_equivalent(
        np.array([np.array([np.nan, None], dtype="object"), None], dtype="object"),
        np.array([np.array([np.nan, None], dtype="object"), None], dtype="object"),
        dtype_equal=dtype_equal,
    )
    assert array_equivalent(
        np.array([np.nan, 1 + 1j], dtype="complex"),
        np.array([np.nan, 1 + 1j], dtype="complex"),
        dtype_equal=dtype_equal,
    )
    assert not array_equivalent(
        np.array([np.nan, 1 + 1j], dtype="complex"),
        np.array([np.nan, 1 + 2j], dtype="complex"),
        dtype_equal=dtype_equal,
    )
    assert not array_equivalent(
        np.array([np.nan, 1, np.nan]),
        np.array([np.nan, 2, np.nan]),
        dtype_equal=dtype_equal,
    )
    assert not array_equivalent(
        np.array(["a", "b", "c", "d"]), np.array(["e", "e"]), dtype_equal=dtype_equal
    )
    assert array_equivalent(
        Index([0, np.nan]), Index([0, np.nan]), dtype_equal=dtype_equal
    )
    assert not array_equivalent(
        Index([0, np.nan]), Index([1, np.nan]), dtype_equal=dtype_equal
    )

