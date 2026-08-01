
def test_dataframe_reductions(op):
    # https://github.com/pandas-dev/pandas/pull/32867
    # ensure the integers are not cast to float during reductions
    df = pd.DataFrame({"a": pd.array([1, 2], dtype="Int64")})
    result = df.max()
    assert isinstance(result["a"], np.int64)


def test_dataframe_reductions(op, expected):
    df = DataFrame({"a": array([1, 2], dtype="Int64")})
    result = getattr(df, op)()
    tm.assert_series_equal(result, expected)

