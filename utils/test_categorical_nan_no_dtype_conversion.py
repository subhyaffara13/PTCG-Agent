
def test_categorical_nan_no_dtype_conversion():
    # GH 43996

    df = pd.DataFrame({"a": Categorical([np.nan], [1]), "b": [1]})
    expected = pd.DataFrame({"a": Categorical([1], [1]), "b": [1]})
    df.loc[0, "a"] = np.array([1])
    tm.assert_frame_equal(df, expected)

