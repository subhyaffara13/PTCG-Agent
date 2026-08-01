
def test_grouby_agg_loses_results_with_as_index_false_relabel_multiindex():
    # GH 32240: When the aggregate function relabels column names and
    # as_index=False is specified, the results are dropped. Check if
    # multiindex is returned in the right order

    df = DataFrame(
        {
            "key": ["x", "y", "x", "y", "x", "x"],
            "key1": ["a", "b", "c", "b", "a", "c"],
            "val": [1.0, 0.8, 2.0, 3.0, 3.6, 0.75],
        }
    )

    grouped = df.groupby(["key", "key1"], as_index=False)
    result = grouped.agg(min_val=pd.NamedAgg(column="val", aggfunc="min"))
    expected = DataFrame(
        {"key": ["x", "x", "y"], "key1": ["a", "c", "b"], "min_val": [1.0, 0.75, 0.8]}
    )
    tm.assert_frame_equal(result, expected)

