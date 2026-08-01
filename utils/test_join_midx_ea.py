
def test_join_midx_ea():
    # GH#49277
    midx = MultiIndex.from_arrays(
        [Series([1, 1, 3], dtype="Int64"), Series([1, 2, 3], dtype="Int64")],
        names=["a", "b"],
    )
    midx2 = MultiIndex.from_arrays(
        [Series([1], dtype="Int64"), Series([3], dtype="Int64")], names=["a", "c"]
    )
    result = midx.join(midx2, how="inner")
    expected = MultiIndex.from_arrays(
        [
            Series([1, 1], dtype="Int64"),
            Series([1, 2], dtype="Int64"),
            Series([3, 3], dtype="Int64"),
        ],
        names=["a", "b", "c"],
    )
    tm.assert_index_equal(result, expected)

