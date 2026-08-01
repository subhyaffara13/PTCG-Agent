
def test_array_equivalent_tdi(dtype_equal):
    assert array_equivalent(
        TimedeltaIndex([0, np.nan]),
        TimedeltaIndex([0, np.nan]),
        dtype_equal=dtype_equal,
    )
    assert not array_equivalent(
        TimedeltaIndex([0, np.nan]),
        TimedeltaIndex([1, np.nan]),
        dtype_equal=dtype_equal,
    )

