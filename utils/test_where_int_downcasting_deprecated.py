
def test_where_int_downcasting_deprecated():
    # GH#44597
    arr = np.arange(6).astype(np.int16).reshape(3, 2)
    df = DataFrame(arr)

    mask = np.zeros(arr.shape, dtype=bool)
    mask[:, 0] = True

    res = df.where(mask, 2**17)

    expected = DataFrame({0: arr[:, 0], 1: np.array([2**17] * 3, dtype=np.int32)})
    tm.assert_frame_equal(res, expected)

