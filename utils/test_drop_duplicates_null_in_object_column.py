
def test_drop_duplicates_null_in_object_column(nulls_fixture):
    # https://github.com/pandas-dev/pandas/issues/32992
    df = DataFrame([[1, nulls_fixture], [2, "a"]], dtype=object)
    result = df.drop_duplicates()
    tm.assert_frame_equal(result, df)

