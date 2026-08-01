
def test_reindex_like_nearest():
    ser = Series(np.arange(10, dtype="int64"))

    target = [0.1, 0.9, 1.5, 2.0]
    other = ser.reindex(target, method="nearest")
    expected = Series(np.around(target).astype("int64"), target)

    with tm.assert_produces_warning(Pandas4Warning):
        result = ser.reindex_like(other, method="nearest")
    tm.assert_series_equal(expected, result)

    with tm.assert_produces_warning(Pandas4Warning):
        result = ser.reindex_like(other, method="nearest", tolerance=1)
    tm.assert_series_equal(expected, result)
    with tm.assert_produces_warning(Pandas4Warning):
        result = ser.reindex_like(other, method="nearest", tolerance=[1, 2, 3, 4])
    tm.assert_series_equal(expected, result)

