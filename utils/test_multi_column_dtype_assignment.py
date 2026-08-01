
def test_multi_column_dtype_assignment():
    # GH #27583
    df = pd.DataFrame({"a": [0.0], "b": 0.0})
    expected = pd.DataFrame({"a": [0], "b": 0})

    df[["a", "b"]] = 0
    tm.assert_frame_equal(df, expected)

    df["b"] = 0
    tm.assert_frame_equal(df, expected)

