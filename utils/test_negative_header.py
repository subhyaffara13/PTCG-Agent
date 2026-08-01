
def test_negative_header(all_parsers):
    # see gh-27779
    parser = all_parsers
    data = """1,2,3,4,5
6,7,8,9,10
11,12,13,14,15
"""
    with pytest.raises(
        ValueError,
        match="Passing negative integer to header is invalid. "
        "For no header, use header=None instead",
    ):
        parser.read_csv(StringIO(data), header=-1)

