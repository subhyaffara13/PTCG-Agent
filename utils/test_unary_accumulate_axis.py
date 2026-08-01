
def test_unary_accumulate_axis():
    # https://github.com/pandas-dev/pandas/issues/39259
    df = pd.DataFrame({"a": [1, 3, 2, 4]})
    result = np.maximum.accumulate(df)
    expected = pd.DataFrame({"a": [1, 3, 3, 4]})
    tm.assert_frame_equal(result, expected)

    df = pd.DataFrame({"a": [1, 3, 2, 4], "b": [0.1, 4.0, 3.0, 2.0]})
    result = np.maximum.accumulate(df)
    # in theory could preserve int dtype for default axis=0
    expected = pd.DataFrame({"a": [1.0, 3.0, 3.0, 4.0], "b": [0.1, 4.0, 4.0, 4.0]})
    tm.assert_frame_equal(result, expected)

    result = np.maximum.accumulate(df, axis=0)
    tm.assert_frame_equal(result, expected)

    result = np.maximum.accumulate(df, axis=1)
    expected = pd.DataFrame({"a": [1.0, 3.0, 2.0, 4.0], "b": [1.0, 4.0, 3.0, 4.0]})
    tm.assert_frame_equal(result, expected)

