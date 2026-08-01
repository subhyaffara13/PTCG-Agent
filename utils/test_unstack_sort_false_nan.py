
def test_unstack_sort_false_nan(levels2, expected_columns):
    # GH#61221
    levels1 = ["b", "a"]
    index = MultiIndex.from_product([levels1, levels2], names=["level1", "level2"])
    df = DataFrame({"value": [0, 1, 2, 3, 4, 5, 6, 7]}, index=index)
    result = df.unstack(level="level2", sort=False)
    expected_data = [[0, 4], [1, 5], [2, 6], [3, 7]]
    expected = DataFrame(
        dict(zip(expected_columns, expected_data)),
        index=Index(["b", "a"], name="level1"),
        columns=MultiIndex.from_tuples(expected_columns, names=[None, "level2"]),
    )
    tm.assert_frame_equal(result, expected)

