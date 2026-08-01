
def test_cross_type_arithmetic():
    df = pd.DataFrame(
        {
            "A": pd.array([1, 2, pd.NA], dtype="Float64"),
            "B": pd.array([1, pd.NA, 3], dtype="Float32"),
            "C": np.array([1, 2, 3], dtype="float64"),
        }
    )

    result = df.A + df.C
    expected = pd.Series([2, 4, pd.NA], dtype="Float64")
    tm.assert_series_equal(result, expected)

    result = (df.A + df.C) * 3 == 12
    expected = pd.Series([False, True, None], dtype="boolean")
    tm.assert_series_equal(result, expected)

    result = df.A + df.B
    expected = pd.Series([2, pd.NA, pd.NA], dtype="Float64")
    tm.assert_series_equal(result, expected)


def test_cross_type_arithmetic():
    df = pd.DataFrame(
        {
            "A": pd.Series([1, 2, pd.NA], dtype="Int64"),
            "B": pd.Series([1, pd.NA, 3], dtype="UInt8"),
            "C": [1, 2, 3],
        }
    )

    result = df.A + df.C
    expected = pd.Series([2, 4, pd.NA], dtype="Int64")
    tm.assert_series_equal(result, expected)

    result = (df.A + df.C) * 3 == 12
    expected = pd.Series([False, True, None], dtype="boolean")
    tm.assert_series_equal(result, expected)

    result = df.A + df.B
    expected = pd.Series([2, pd.NA, pd.NA], dtype="Int64")
    tm.assert_series_equal(result, expected)

