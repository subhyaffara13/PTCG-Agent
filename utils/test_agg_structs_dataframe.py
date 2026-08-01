
def test_agg_structs_dataframe(structure, cast_as):
    df = DataFrame(
        {"A": [1, 1, 1, 3, 3, 3], "B": [1, 1, 1, 4, 4, 4], "C": [1, 1, 1, 3, 4, 4]}
    )

    result = df.groupby(["A", "B"]).aggregate(structure)
    expected = DataFrame(
        {"C": {(1, 1): cast_as([1, 1, 1]), (3, 4): cast_as([3, 4, 4])}}
    )
    expected.index.names = ["A", "B"]
    tm.assert_frame_equal(result, expected)

