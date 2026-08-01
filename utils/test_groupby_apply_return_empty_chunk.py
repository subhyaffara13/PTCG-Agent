
def test_groupby_apply_return_empty_chunk():
    # GH 22221: apply filter which returns some empty groups
    df = DataFrame({"value": [0, 1], "group": ["filled", "empty"]})
    groups = df.groupby("group")
    result = groups.apply(lambda group: group[group.value != 1]["value"])
    expected = Series(
        [0],
        name="value",
        index=MultiIndex.from_product(
            [["empty", "filled"], [0]], names=["group", None]
        ).drop("empty"),
    )
    tm.assert_series_equal(result, expected)

