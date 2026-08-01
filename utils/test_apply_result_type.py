
def test_apply_result_type(group_keys, udf):
    # https://github.com/pandas-dev/pandas/issues/34809
    # We'd like to control whether the group keys end up in the index
    # regardless of whether the UDF happens to be a transform.
    df = DataFrame({"A": ["a", "b"], "B": [1, 2]})
    df_result = df.groupby("A", group_keys=group_keys).apply(udf)
    series_result = df.B.groupby(df.A, group_keys=group_keys).apply(udf)

    if group_keys:
        assert df_result.index.nlevels == 2
        assert series_result.index.nlevels == 2
    else:
        assert df_result.index.nlevels == 1
        assert series_result.index.nlevels == 1

