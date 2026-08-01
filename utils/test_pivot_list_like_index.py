
def test_pivot_list_like_index(
    input_index,
    input_columns,
    input_values,
    expected_values,
    expected_columns,
    expected_index,
):
    # GH 21425, test when index is given a list
    df = pd.DataFrame(
        {
            "lev1": [1, 1, 1, 1, 2, 2, 2, 2],
            "lev2": [1, 1, 2, 2, 1, 1, 2, 2],
            "lev3": [1, 2, 1, 2, 1, 2, 1, 2],
            "lev4": [1, 2, 3, 4, 5, 6, 7, 8],
            "values": [0, 1, 2, 3, 4, 5, 6, 7],
        }
    )

    result = df.pivot(index=input_index, columns=input_columns, values=input_values)
    expected = pd.DataFrame(
        expected_values, columns=expected_columns, index=expected_index
    )
    tm.assert_frame_equal(result, expected)

