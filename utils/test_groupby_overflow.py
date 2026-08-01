
def test_groupby_overflow(val, dtype):
    # GH#37493
    df = DataFrame({"a": 1, "b": [val, val]}, dtype=f"{dtype}8")
    result = df.groupby("a").sum()
    expected = DataFrame(
        {"b": [val * 2]},
        index=Index([1], name="a", dtype=f"{dtype}8"),
        dtype=f"{dtype}64",
    )
    tm.assert_frame_equal(result, expected)

    result = df.groupby("a").cumsum()
    expected = DataFrame({"b": [val, val * 2]}, dtype=f"{dtype}64")
    tm.assert_frame_equal(result, expected)

    result = df.groupby("a").prod()
    expected = DataFrame(
        {"b": [val * val]},
        index=Index([1], name="a", dtype=f"{dtype}8"),
        dtype=f"{dtype}64",
    )
    tm.assert_frame_equal(result, expected)

