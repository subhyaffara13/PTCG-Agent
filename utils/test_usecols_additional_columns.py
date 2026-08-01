
def test_usecols_additional_columns(all_parsers):
    # GH#46997
    parser = all_parsers
    usecols = lambda header: header.strip() in ["a", "b", "c"]

    if parser.engine == "pyarrow":
        msg = "The pyarrow engine does not allow 'usecols' to be a callable"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO("a,b\nx,y,z"), index_col=False, usecols=usecols)
        return
    result = parser.read_csv(StringIO("a,b\nx,y,z"), index_col=False, usecols=usecols)
    expected = DataFrame({"a": ["x"], "b": "y"})
    tm.assert_frame_equal(result, expected)

