
def test_agg_structs_series(structure, cast_as):
    # Issue #18079
    df = DataFrame(
        {"A": [1, 1, 1, 3, 3, 3], "B": [1, 1, 1, 4, 4, 4], "C": [1, 1, 1, 3, 4, 4]}
    )

    result = df.groupby("A")["C"].aggregate(structure)
    expected = Series([cast_as([1, 1, 1]), cast_as([3, 4, 4])], index=[1, 3], name="C")
    expected.index.name = "A"
    tm.assert_series_equal(result, expected)

