
def test_groupby_dropna_with_nunique_unique():
    # GH#42016
    df = [[1, 1, 1, "A"], [1, None, 1, "A"], [1, None, 2, "A"], [1, None, 3, "A"]]
    df_dropna = DataFrame(df, columns=["a", "b", "c", "partner"])
    result = df_dropna.groupby(["a", "b", "c"], dropna=False).agg(
        {"partner": ["nunique", "unique"]}
    )

    index = MultiIndex.from_tuples(
        [(1, 1.0, 1), (1, np.nan, 1), (1, np.nan, 2), (1, np.nan, 3)],
        names=["a", "b", "c"],
    )
    columns = MultiIndex.from_tuples([("partner", "nunique"), ("partner", "unique")])
    expected = DataFrame(
        [(1, ["A"]), (1, ["A"]), (1, ["A"]), (1, ["A"])], index=index, columns=columns
    )

    tm.assert_frame_equal(result, expected)

