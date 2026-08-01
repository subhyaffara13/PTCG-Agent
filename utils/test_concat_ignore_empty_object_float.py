
def test_concat_ignore_empty_object_float(empty_dtype, df_dtype):
    # https://github.com/pandas-dev/pandas/issues/45637
    df = DataFrame({"foo": [1, 2], "bar": [1, 2]}, dtype=df_dtype)
    empty = DataFrame(columns=["foo", "bar"], dtype=empty_dtype)

    needs_update = False
    if df_dtype == "datetime64[ns]" or (
        df_dtype == "float64" and empty_dtype != "float64"
    ):
        needs_update = True

    result = concat([empty, df])
    expected = df
    if df_dtype == "int64":
        # TODO what exact behaviour do we want for integer eventually?
        if empty_dtype == "float64":
            expected = df.astype("float64")
        else:
            expected = df.astype("object")

    if needs_update:
        # GH#40893 changed the expected here to retain dependence on empty
        expected = expected.astype(object)
    tm.assert_frame_equal(result, expected)

