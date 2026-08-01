
def test_observed(observed, using_infer_string):
    # multiple groupers, don't re-expand the output space
    # of the grouper
    # gh-14942 (implement)
    # gh-10132 (back-compat)
    # gh-8138 (back-compat)
    # gh-8869

    cat1 = Categorical(["a", "a", "b", "b"], categories=["a", "b", "z"], ordered=True)
    cat2 = Categorical(["c", "d", "c", "d"], categories=["c", "d", "y"], ordered=True)
    df = DataFrame({"A": cat1, "B": cat2, "values": [1, 2, 3, 4]})
    df["C"] = ["foo", "bar"] * 2

    # multiple groupers with a non-cat
    gb = df.groupby(["A", "B", "C"], observed=observed)
    exp_index = MultiIndex.from_arrays(
        [cat1, cat2, ["foo", "bar"] * 2], names=["A", "B", "C"]
    )
    expected = DataFrame({"values": Series([1, 2, 3, 4], index=exp_index)}).sort_index()
    result = gb.sum()
    if not observed:
        expected = cartesian_product_for_groupers(
            expected, [cat1, cat2, ["foo", "bar"]], list("ABC"), fill_value=0
        )

    tm.assert_frame_equal(result, expected)

    gb = df.groupby(["A", "B"], observed=observed)
    exp_index = MultiIndex.from_arrays([cat1, cat2], names=["A", "B"])
    expected = DataFrame(
        {"values": [1, 2, 3, 4], "C": ["foo", "bar", "foo", "bar"]}, index=exp_index
    )
    result = gb.sum()
    if not observed:
        expected = cartesian_product_for_groupers(
            expected,
            [cat1, cat2],
            list("AB"),
            fill_value={"values": 0, "C": ""} if using_infer_string else 0,
        )

    tm.assert_frame_equal(result, expected)

