
def test_nth_empty():
    # GH 16064
    df = DataFrame(index=[0], columns=["a", "b", "c"])
    result = df.groupby("a").nth(10)
    expected = df.iloc[:0]
    tm.assert_frame_equal(result, expected)

    result = df.groupby(["a", "b"]).nth(10)
    expected = df.iloc[:0]
    tm.assert_frame_equal(result, expected)

