
def test_groupby_categorical_aggregate_functions():
    # GH#37275
    dtype = pd.CategoricalDtype(categories=["small", "big"], ordered=True)
    df = DataFrame(
        [[1, "small"], [1, "big"], [2, "small"]], columns=["grp", "description"]
    ).astype({"description": dtype})

    result = df.groupby("grp")["description"].max()
    expected = Series(
        ["big", "small"],
        index=Index([1, 2], name="grp"),
        name="description",
        dtype=pd.CategoricalDtype(categories=["small", "big"], ordered=True),
    )

    tm.assert_series_equal(result, expected)

