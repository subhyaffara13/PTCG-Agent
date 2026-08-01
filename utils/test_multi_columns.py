
def test_multi_columns(input_subset, expected_dict, expected_index):
    # GH 39240
    df = pd.DataFrame(
        {
            "A": [[0, 1, 2], np.nan, [], (3, 4), np.nan],
            "B": 1,
            "C": [["a", "b", "c"], "foo", [], ["d", "e"], np.nan],
        },
        index=list("abcde"),
    )
    result = df.explode(input_subset)
    expected = pd.DataFrame(expected_dict, expected_index)
    tm.assert_frame_equal(result, expected)

