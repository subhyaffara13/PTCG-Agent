
def test_empty_groups_corner(multiindex_dataframe_random_data):
    # handle empty groups
    df = DataFrame(
        {
            "k1": np.array(["b", "b", "b", "a", "a", "a"]),
            "k2": np.array(["1", "1", "1", "2", "2", "2"]),
            "k3": ["foo", "bar"] * 3,
            "v1": np.random.default_rng(2).standard_normal(6),
            "v2": np.random.default_rng(2).standard_normal(6),
        }
    )

    grouped = df.groupby(["k1", "k2"])
    result = grouped[["v1", "v2"]].agg("mean")
    expected = grouped.mean(numeric_only=True)
    tm.assert_frame_equal(result, expected)

    grouped = multiindex_dataframe_random_data[3:5].groupby(level=0)
    agged = grouped.apply(lambda x: x.mean())
    agged_A = grouped["A"].apply("mean")
    tm.assert_series_equal(agged["A"], agged_A)
    assert agged.index.name == "first"

