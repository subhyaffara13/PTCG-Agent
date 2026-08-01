
def test_to_frame_resulting_column_order():
    # GH 22420
    expected = ["z", 0, "a"]
    mi = MultiIndex.from_arrays(
        [["a", "b", "c"], ["x", "y", "z"], ["q", "w", "e"]], names=expected
    )
    result = mi.to_frame().columns.tolist()
    assert result == expected

