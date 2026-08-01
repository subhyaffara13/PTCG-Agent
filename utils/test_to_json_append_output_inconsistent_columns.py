
def test_to_json_append_output_inconsistent_columns(temp_file):
    # GH 35849
    # Testing that resulting output reads in as expected.
    # Testing one new column, one old column, new rows
    df1 = DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    df3 = DataFrame({"col2": ["e", "f"], "col3": ["!", "#"]})

    expected = DataFrame(
        {
            "col1": [1, 2, None, None],
            "col2": ["a", "b", "e", "f"],
            "col3": [np.nan, np.nan, "!", "#"],
        }
    )
    # Save dataframes to the same file
    df1.to_json(temp_file, mode="a", lines=True, orient="records")
    df3.to_json(temp_file, mode="a", lines=True, orient="records")

    # Read path file
    result = read_json(temp_file, lines=True)
    tm.assert_frame_equal(result, expected)

