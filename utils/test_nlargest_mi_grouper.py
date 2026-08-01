
def test_nlargest_mi_grouper():
    # see gh-21411
    npr = np.random.default_rng(2)

    dts = date_range("20180101", periods=10)
    iterables = [dts, ["one", "two"]]

    idx = MultiIndex.from_product(iterables, names=["first", "second"])
    s = Series(npr.standard_normal(20), index=idx)

    result = s.groupby("first").nlargest(1)

    exp_idx = MultiIndex.from_tuples(
        [
            (dts[0], dts[0], "one"),
            (dts[1], dts[1], "one"),
            (dts[2], dts[2], "one"),
            (dts[3], dts[3], "two"),
            (dts[4], dts[4], "one"),
            (dts[5], dts[5], "one"),
            (dts[6], dts[6], "one"),
            (dts[7], dts[7], "one"),
            (dts[8], dts[8], "one"),
            (dts[9], dts[9], "one"),
        ],
        names=["first", "first", "second"],
    )

    exp_values = [
        0.18905338179353307,
        -0.41306354339189344,
        1.799707382720902,
        0.7738065867276614,
        0.28121066979764925,
        0.9775674511260357,
        -0.3288239040579627,
        0.45495807124085547,
        0.5452887139646817,
        0.12682784711186987,
    ]

    expected = Series(exp_values, index=exp_idx)
    tm.assert_series_equal(result, expected, check_exact=False, rtol=1e-3)

