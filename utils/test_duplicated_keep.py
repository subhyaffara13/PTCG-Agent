
def test_duplicated_keep(keep, expected):
    ser = Series(["a", "b", "b", "c", "a"], name="name")

    result = ser.duplicated(keep=keep)
    expected = Series(expected, name="name")
    tm.assert_series_equal(result, expected)


def test_duplicated_keep(keep, expected):
    df = DataFrame({"A": [0, 1, 1, 2, 0], "B": ["a", "b", "b", "c", "a"]})

    result = df.duplicated(keep=keep)
    tm.assert_series_equal(result, expected)

