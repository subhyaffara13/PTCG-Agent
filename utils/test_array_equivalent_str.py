
def test_array_equivalent_str(dtype):
    assert array_equivalent(
        np.array(["A", "B"], dtype=dtype), np.array(["A", "B"], dtype=dtype)
    )
    assert not array_equivalent(
        np.array(["A", "B"], dtype=dtype), np.array(["A", "X"], dtype=dtype)
    )

