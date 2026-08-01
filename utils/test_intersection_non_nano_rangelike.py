
def test_intersection_non_nano_rangelike():
    # GH 59271
    l1 = date_range("2024-01-01", "2024-01-03", unit="s")
    l2 = date_range("2024-01-02", "2024-01-04", unit="s")
    result = l1.intersection(l2)
    expected = DatetimeIndex(
        ["2024-01-02", "2024-01-03"],
        dtype="datetime64[s]",
        freq="D",
    )
    tm.assert_index_equal(result, expected)

