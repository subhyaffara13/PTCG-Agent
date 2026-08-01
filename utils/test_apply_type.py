
def test_apply_type():
    # GH 46719
    df = DataFrame(
        {"col1": [3, "string", float], "col2": [0.25, datetime(2020, 1, 1), np.nan]},
        index=["a", "b", "c"],
    )

    # axis=0
    result = df.apply(type, axis=0)
    expected = Series({"col1": Series, "col2": Series})
    tm.assert_series_equal(result, expected)

    # axis=1
    result = df.apply(type, axis=1)
    expected = Series({"a": Series, "b": Series, "c": Series})
    tm.assert_series_equal(result, expected)


def test_apply_type():
    # GH 46719
    s = Series([3, "string", float], index=["a", "b", "c"])
    result = s.apply(type)
    expected = Series([int, str, type], index=["a", "b", "c"])
    tm.assert_series_equal(result, expected)

