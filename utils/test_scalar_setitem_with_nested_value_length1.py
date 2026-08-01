
def test_scalar_setitem_with_nested_value_length1(value):
    # https://github.com/pandas-dev/pandas/issues/46268

    # For numeric data, assigning length-1 array to scalar position gets unpacked
    df = DataFrame({"A": [1, 2, 3]})
    df.loc[0, "B"] = value
    expected = DataFrame({"A": [1, 2, 3], "B": [0.0, np.nan, np.nan]})
    tm.assert_frame_equal(df, expected)

    # but for object dtype we preserve the nested data
    df = DataFrame({"A": [1, 2, 3], "B": np.array([1, "a", "b"], dtype=object)})
    df.loc[0, "B"] = value
    if isinstance(value, np.ndarray):
        assert (df.loc[0, "B"] == value).all()
    else:
        assert df.loc[0, "B"] == value

