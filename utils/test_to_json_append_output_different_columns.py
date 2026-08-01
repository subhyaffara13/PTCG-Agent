
def test_to_json_append_output_different_columns(temp_file):
    # GH 35849
    # Testing that resulting output reads in as expected.
    # Testing same, differing and new columns
    df1 = DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    df2 = DataFrame({"col1": [3, 4], "col2": ["c", "d"]})
    df3 = DataFrame({"col2": ["e", "f"], "col3": ["!", "#"]})
    df4 = DataFrame({"col4": [True, False]})

    expected = DataFrame(
        {
            "col1": [1, 2, 3, 4, None, None, None, None],
            "col2": ["a", "b", "c", "d", "e", "f", np.nan, np.nan],
            "col3": [np.nan, np.nan, np.nan, np.nan, "!", "#", np.nan, np.nan],
            "col4": [None, None, None, None, None, None, True, False],
        }
    ).astype({"col4": "float"})
    # Save dataframes to the same file
    df1.to_json(temp_file, mode="a", lines=True, orient="records")
    df2.to_json(temp_file, mode="a", lines=True, orient="records")
    df3.to_json(temp_file, mode="a", lines=True, orient="records")
    df4.to_json(temp_file, mode="a", lines=True, orient="records")

    # Read path file
    result = read_json(temp_file, lines=True)
    tm.assert_frame_equal(result, expected)

