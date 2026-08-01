
def test_apply_broadcast_error(func):
    df = DataFrame(
        np.tile(np.arange(3, dtype="int64"), 6).reshape(6, -1) + 1,
        columns=["A", "B", "C"],
    )

    # > 1 ndim
    msg = "too many dims to broadcast|cannot broadcast result"
    with pytest.raises(ValueError, match=msg):
        df.apply(func, axis=1, result_type="broadcast")

