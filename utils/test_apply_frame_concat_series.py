
def test_apply_frame_concat_series():
    def trans(group):
        return group.groupby("B")["C"].sum().sort_values().iloc[:2]

    def trans2(group):
        grouped = group.groupby(df.reindex(group.index)["B"])
        return grouped.sum().sort_values().iloc[:2]

    df = DataFrame(
        {
            "A": np.random.default_rng(2).integers(0, 5, 1000),
            "B": np.random.default_rng(2).integers(0, 5, 1000),
            "C": np.random.default_rng(2).standard_normal(1000),
        }
    )

    result = df.groupby("A").apply(trans)
    exp = df.groupby("A")["C"].apply(trans2)
    tm.assert_series_equal(result, exp, check_names=False)
    assert result.name == "C"

