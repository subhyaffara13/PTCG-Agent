
def test_demo():
    # demonstration tests
    df = DataFrame({"A": range(5), "B": 5})

    result = df.agg(["min", "max"])
    expected = DataFrame(
        {"A": [0, 4], "B": [5, 5]}, columns=["A", "B"], index=["min", "max"]
    )
    tm.assert_frame_equal(result, expected)


def test_demo():
    # demonstration tests
    s = Series(range(6), dtype="int64", name="series")

    result = s.agg(["min", "max"])
    expected = Series([0, 5], index=["min", "max"], name="series")
    tm.assert_series_equal(result, expected)

    result = s.agg({"foo": "min"})
    expected = Series([0], index=["foo"], name="series")
    tm.assert_series_equal(result, expected)

