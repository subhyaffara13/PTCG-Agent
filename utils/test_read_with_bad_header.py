
def test_read_with_bad_header(all_parsers):
    parser = all_parsers
    msg = r"but only \d+ lines in file"

    with pytest.raises(ValueError, match=msg):
        parser.read_csv(StringIO(",,"), header=[10])

