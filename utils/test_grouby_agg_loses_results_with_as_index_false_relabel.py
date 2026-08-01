
def test_grouby_agg_loses_results_with_as_index_false_relabel():
    # GH 32240: When the aggregate function relabels column names and
    # as_index=False is specified, the results are dropped.

    df = DataFrame(
        {"key": ["x", "y", "z", "x", "y", "z"], "val": [1.0, 0.8, 2.0, 3.0, 3.6, 0.75]}
    )

    grouped = df.groupby("key", as_index=False)
    result = grouped.agg(min_val=pd.NamedAgg(column="val", aggfunc="min"))
    expected = DataFrame({"key": ["x", "y", "z"], "min_val": [1.0, 0.8, 0.75]})
    tm.assert_frame_equal(result, expected)

