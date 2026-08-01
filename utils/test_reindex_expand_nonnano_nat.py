
def test_reindex_expand_nonnano_nat(dtype):
    # GH 53497
    ser = Series(np.array([1], dtype=f"{dtype}[s]"))
    result = ser.reindex(RangeIndex(2))
    expected = Series(
        np.array([1, getattr(np, dtype)("nat", "s")], dtype=f"{dtype}[s]")
    )
    tm.assert_series_equal(result, expected)

