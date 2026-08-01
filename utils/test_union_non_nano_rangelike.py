
def test_union_non_nano_rangelike():
    # GH 59036
    l1 = DatetimeIndex(
        ["2024-05-11", "2024-05-12"], dtype="datetime64[us]", name="Date", freq="D"
    )
    l2 = DatetimeIndex(["2024-05-13"], dtype="datetime64[us]", name="Date", freq="D")
    result = l1.union(l2)
    expected = DatetimeIndex(
        ["2024-05-11", "2024-05-12", "2024-05-13"],
        dtype="datetime64[us]",
        name="Date",
        freq="D",
    )
    tm.assert_index_equal(result, expected)

