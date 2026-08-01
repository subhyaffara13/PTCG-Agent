
def test_multi_columns_nan_empty():
    # GH 46084
    df = pd.DataFrame(
        {
            "A": [[0, 1], [5], [], [2, 3]],
            "B": [9, 8, 7, 6],
            "C": [[1, 2], np.nan, [], [3, 4]],
        }
    )
    result = df.explode(["A", "C"])
    expected = pd.DataFrame(
        {
            "A": np.array([0, 1, 5, np.nan, 2, 3], dtype=object),
            "B": [9, 9, 8, 7, 6, 6],
            "C": np.array([1, 2, np.nan, np.nan, 3, 4], dtype=object),
        },
        index=[0, 0, 1, 2, 3, 3],
    )
    tm.assert_frame_equal(result, expected)

