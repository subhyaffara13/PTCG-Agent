
def test_cython_with_timestamp_and_nat(op, data):
    # https://github.com/pandas-dev/pandas/issues/19526
    df = DataFrame({"a": [0, 1], "b": [data, NaT]})
    index = Index([0, 1], name="a")

    # We will group by a and test the cython aggregations
    expected = DataFrame({"b": [data, NaT]}, index=index)

    result = df.groupby("a").aggregate(op)
    tm.assert_frame_equal(expected, result)

