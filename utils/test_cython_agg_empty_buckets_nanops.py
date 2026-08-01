
def test_cython_agg_empty_buckets_nanops(observed):
    # GH-18869 can't call nanops on empty groups, so hardcode expected
    # for these
    df = DataFrame([11, 12, 13], columns=["a"])
    grps = np.arange(0, 25, 5, dtype=int)
    # add / sum
    result = df.groupby(pd.cut(df["a"], grps), observed=observed)._cython_agg_general(
        "sum", alt=None, numeric_only=True
    )
    intervals = pd.interval_range(0, 20, freq=5)
    expected = DataFrame(
        {"a": [0, 0, 36, 0]},
        index=pd.CategoricalIndex(intervals, name="a", ordered=True),
    )
    if observed:
        expected = expected[expected.a != 0]

    tm.assert_frame_equal(result, expected)

    # prod
    result = df.groupby(pd.cut(df["a"], grps), observed=observed)._cython_agg_general(
        "prod", alt=None, numeric_only=True
    )
    expected = DataFrame(
        {"a": [1, 1, 1716, 1]},
        index=pd.CategoricalIndex(intervals, name="a", ordered=True),
    )
    if observed:
        expected = expected[expected.a != 1]

    tm.assert_frame_equal(result, expected)

