
def test_len_colspecs_len_names(colspecs, names, widths, index_col):
    # GH#40830
    data = """col1  col2  col3  col4
    bab   ba    2"""
    msg = "Length of colspecs must match length of names"
    with pytest.raises(ValueError, match=msg):
        read_fwf(
            StringIO(data),
            colspecs=colspecs,
            names=names,
            widths=widths,
            index_col=index_col,
        )

