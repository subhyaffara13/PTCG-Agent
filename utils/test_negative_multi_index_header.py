
def test_negative_multi_index_header(all_parsers, header):
    # see gh-27779
    parser = all_parsers
    data = """1,2,3,4,5
        6,7,8,9,10
        11,12,13,14,15
        """
    with pytest.raises(
        ValueError, match="cannot specify multi-index header with negative integers"
    ):
        parser.read_csv(StringIO(data), header=header)

