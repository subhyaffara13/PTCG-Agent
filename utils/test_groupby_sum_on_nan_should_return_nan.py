
def test_groupby_sum_on_nan_should_return_nan(bug_var):
    # GH 24196
    df = DataFrame({"A": [bug_var, bug_var, bug_var, np.nan]})
    if isinstance(bug_var, str):
        df = df.astype(object)
    dfgb = df.groupby(lambda x: x)
    result = dfgb.sum(min_count=1)

    expected_df = DataFrame(
        [bug_var, bug_var, bug_var, None], columns=["A"], dtype=df["A"].dtype
    )
    tm.assert_frame_equal(result, expected_df)

