
def test_aggregate_udf_na_extension_type():
    # https://github.com/pandas-dev/pandas/pull/31359
    # This is currently failing to cast back to Int64Dtype.
    # The presence of the NA causes two problems
    # 1. NA is not an instance of Int64Dtype.type (numpy.int64)
    # 2. The presence of an NA forces object type, so the non-NA values is
    #    a Python int rather than a NumPy int64. Python ints aren't
    #    instances of numpy.int64.
    def aggfunc(x):
        if all(x > 2):
            return 1
        else:
            return pd.NA

    df = DataFrame({"A": pd.array([1, 2, 3])})
    result = df.groupby([1, 1, 2]).agg(aggfunc)
    expected = DataFrame({"A": pd.array([1, pd.NA], dtype="Int64")}, index=[1, 2])
    tm.assert_frame_equal(result, expected)

