
def test_converter_index_col_bug(all_parsers, conv_f):
    # see gh-1835 , GH#40589
    parser = all_parsers
    data = "A;B\n1;2\n3;4"

    if parser.engine == "pyarrow":
        msg = "The 'converters' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(
                StringIO(data), sep=";", index_col="A", converters={"A": conv_f}
            )
        return

    rs = parser.read_csv(
        StringIO(data), sep=";", index_col="A", converters={"A": conv_f}
    )

    xp = DataFrame({"B": [2, 4]}, index=Index(["1", "3"], name="A"))
    tm.assert_frame_equal(rs, xp)

