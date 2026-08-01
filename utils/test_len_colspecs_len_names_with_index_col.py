
def test_len_colspecs_len_names_with_index_col(
    colspecs, names, widths, index_col, expected
):
    # GH#40830
    data = """col1  col2  col3  col4
    bab   ba    2"""
    result = read_fwf(
        StringIO(data),
        colspecs=colspecs,
        names=names,
        widths=widths,
        index_col=index_col,
    )
    tm.assert_frame_equal(result, expected)

