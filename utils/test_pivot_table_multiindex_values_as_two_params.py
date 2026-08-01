
def test_pivot_table_multiindex_values_as_two_params(
    index, columns, e_data, e_index, e_cols
):
    # GH#61292
    data = [
        ["A", 1, 50, -1],
        ["B", 1, 100, -2],
        ["A", 2, 100, -2],
        ["B", 2, 200, -4],
    ]
    df = pd.DataFrame(data=data, columns=["index", "col", "value", "extra"])
    result = df.pivot_table(values="value", index=index, columns=columns)
    expected = pd.DataFrame(data=e_data, index=e_index, columns=e_cols)
    tm.assert_frame_equal(result, expected)

