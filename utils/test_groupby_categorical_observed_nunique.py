
def test_groupby_categorical_observed_nunique():
    # GH#45128
    df = DataFrame({"a": [1, 2], "b": [1, 2], "c": [10, 11]})
    df = df.astype(dtype={"a": "category", "b": "category"})
    result = df.groupby(["a", "b"], observed=True).nunique()["c"]
    expected = Series(
        [1, 1],
        index=MultiIndex.from_arrays(
            [CategoricalIndex([1, 2], name="a"), CategoricalIndex([1, 2], name="b")]
        ),
        name="c",
    )
    tm.assert_series_equal(result, expected)

