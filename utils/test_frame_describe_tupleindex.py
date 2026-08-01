
def test_frame_describe_tupleindex():
    # GH 14848 - regression from 0.19.0 to 0.19.1
    name = "k"
    df = DataFrame(
        {
            "x": [1, 2, 3, 4, 5] * 3,
            name: [(0, 0, 1), (0, 1, 0), (1, 0, 0)] * 5,
        }
    )
    result = df.groupby(name).describe()
    expected = DataFrame(
        [[5.0, 3.0, 1.581139, 1.0, 2.0, 3.0, 4.0, 5.0]] * 3,
        index=Index([(0, 0, 1), (0, 1, 0), (1, 0, 0)], tupleize_cols=False, name=name),
        columns=MultiIndex.from_arrays(
            [["x"] * 8, ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]]
        ),
    )
    tm.assert_frame_equal(result, expected)

