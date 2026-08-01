
def test_compression_error(parser, compression_only, tmp_path):
    path = tmp_path / "geom_xml.zip"
    geom_df.to_xml(path, parser=parser, compression=compression_only)

    with pytest.raises(
        ParserError, match=("iterparse is designed for large XML files")
    ):
        read_xml(
            path,
            parser=parser,
            iterparse={"row": ["shape", "degrees", "sides", "date"]},
            compression=compression_only,
        )

