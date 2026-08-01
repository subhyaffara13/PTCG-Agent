
def test_unsupported_compression(parser, geom_df, temp_file):
    with pytest.raises(ValueError, match="Unrecognized compression type"):
        path = temp_file
        geom_df.to_xml(path, parser=parser, compression="7z")


def test_unsupported_compression(parser, temp_file):
    with pytest.raises(ValueError, match="Unrecognized compression type"):
        read_xml(temp_file, parser=parser, compression="7z")

