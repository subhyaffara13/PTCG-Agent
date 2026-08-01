
def test_to_json_append_output_consistent_columns(temp_file):
    # GH 35849
    # Testing that resulting output reads in as expected.
    # Testing same columns, new rows
    df1 = DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    df2 = DataFrame({"col1": [3, 4], "col2": ["c", "d"]})

    expected = DataFrame({"col1": [1, 2, 3, 4], "col2": ["a", "b", "c", "d"]})
    # Save dataframes to the same file
    df1.to_json(temp_file, lines=True, orient="records")
    df2.to_json(temp_file, mode="a", lines=True, orient="records")

    # Read path file
    result = read_json(temp_file, lines=True)
    tm.assert_frame_equal(result, expected)

