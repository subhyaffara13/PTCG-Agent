
def test_frame_setitem_partial_multiindex():
    # GH 54875
    df = DataFrame(
        {
            "a": [1, 2, 3],
            "b": [3, 4, 5],
            "c": 6,
            "d": 7,
        }
    ).set_index(["a", "b", "c"])
    ser = Series(8, index=df.index.droplevel("c"))
    result = df.copy()
    result["d"] = ser
    expected = df.copy()
    expected["d"] = 8
    tm.assert_frame_equal(result, expected)

