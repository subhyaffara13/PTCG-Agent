
def test_infer_output_shape_listlike_columns_np_func(val):
    # GH 17970
    df = DataFrame({"a": [1, 2, 3]}, index=list("abc"))

    result = df.apply(lambda row: np.ones(val), axis=1)
    expected = Series([np.ones(val) for t in df.itertuples()], index=df.index)
    tm.assert_series_equal(result, expected)

