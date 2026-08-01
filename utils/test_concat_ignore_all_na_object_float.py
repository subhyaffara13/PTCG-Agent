
def test_concat_ignore_all_na_object_float(empty_dtype, df_dtype):
    df = DataFrame({"foo": [1, 2], "bar": [1, 2]}, dtype=df_dtype)
    empty = DataFrame({"foo": [np.nan], "bar": [np.nan]}, dtype=empty_dtype)

    if df_dtype == "int64":
        # TODO what exact behaviour do we want for integer eventually?
        if empty_dtype == "object":
            df_dtype = "object"
        else:
            df_dtype = "float64"

    needs_update = False
    if empty_dtype != df_dtype and empty_dtype is not None:
        needs_update = True
    elif df_dtype == "datetime64[ns]":
        needs_update = True

    result = concat([empty, df], ignore_index=True)

    expected = DataFrame({"foo": [np.nan, 1, 2], "bar": [np.nan, 1, 2]}, dtype=df_dtype)
    if needs_update:
        # GH#40893 changed the expected here to retain dependence on empty
        expected = expected.astype(object)
        expected.iloc[0] = np.nan
    tm.assert_frame_equal(result, expected)

