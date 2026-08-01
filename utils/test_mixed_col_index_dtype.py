
def test_mixed_col_index_dtype(string_dtype_no_object):
    # GH 47382
    df1 = DataFrame(columns=list("abc"), data=1.0, index=[0])
    df2 = DataFrame(columns=list("abc"), data=0.0, index=[0])
    df1.columns = df2.columns.astype(string_dtype_no_object)
    result = df1 + df2
    expected = DataFrame(columns=list("abc"), data=1.0, index=[0])

    expected.columns = expected.columns.astype(string_dtype_no_object)

    tm.assert_frame_equal(result, expected)

