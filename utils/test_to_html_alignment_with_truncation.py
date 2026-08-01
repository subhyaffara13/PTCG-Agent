
def test_to_html_alignment_with_truncation(
    datapath, row_index, row_type, column_index, column_type, index, header, index_names
):
    # GH 22747, GH 22579
    df = DataFrame(np.arange(64).reshape(8, 8), index=row_index, columns=column_index)
    result = df.to_html(
        max_rows=4, max_cols=4, index=index, header=header, index_names=index_names
    )

    if not index:
        row_type = "none"
    elif not index_names and row_type.startswith("named"):
        row_type = "un" + row_type

    if not header:
        column_type = "none"
    elif not index_names and column_type.startswith("named"):
        column_type = "un" + column_type

    filename = "trunc_df_index_" + row_type + "_columns_" + column_type
    expected = expected_html(datapath, filename)
    assert result == expected

