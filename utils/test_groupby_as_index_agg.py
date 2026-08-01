
def test_groupby_as_index_agg(df):
    grouped = df.groupby("A", as_index=False)

    # single-key

    result = grouped[["C", "D"]].agg("mean")
    expected = grouped.mean(numeric_only=True)
    tm.assert_frame_equal(result, expected)

    result2 = grouped.agg({"C": "mean", "D": "sum"})
    expected2 = grouped.mean(numeric_only=True)
    expected2["D"] = grouped.sum()["D"]
    tm.assert_frame_equal(result2, expected2)

    grouped = df.groupby("A", as_index=True)

    msg = r"nested renamer is not supported"
    with pytest.raises(SpecificationError, match=msg):
        grouped["C"].agg({"Q": "sum"})

    # multi-key

    grouped = df.groupby(["A", "B"], as_index=False)

    result = grouped.agg("mean")
    expected = grouped.mean()
    tm.assert_frame_equal(result, expected)

    result2 = grouped.agg({"C": "mean", "D": "sum"})
    expected2 = grouped.mean()
    expected2["D"] = grouped.sum()["D"]
    tm.assert_frame_equal(result2, expected2)

    expected3 = grouped["C"].sum()
    expected3 = DataFrame(expected3).rename(columns={"C": "Q"})
    msg = "nested renamer is not supported"
    with pytest.raises(SpecificationError, match=msg):
        grouped["C"].agg({"Q": "sum"})

    # GH7115 & GH8112 & GH8582
    df = DataFrame(
        np.random.default_rng(2).integers(0, 100, (50, 3)),
        columns=["jim", "joe", "jolie"],
    )
    ts = Series(np.random.default_rng(2).integers(5, 10, 50), name="jim")

    gr = df.groupby(ts)
    gr.nth(0)  # invokes set_selection_from_grouper internally

    for attr in ["mean", "max", "count", "idxmax", "cumsum", "all"]:
        gr = df.groupby(ts, as_index=False)
        left = getattr(gr, attr)()

        gr = df.groupby(ts.values, as_index=True)
        right = getattr(gr, attr)().reset_index(drop=True)

        tm.assert_frame_equal(left, right)

