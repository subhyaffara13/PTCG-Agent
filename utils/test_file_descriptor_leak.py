
def test_file_descriptor_leak(all_parsers, temp_file):
    # GH 31488
    parser = all_parsers
    path = temp_file
    with pytest.raises(EmptyDataError, match="No columns to parse from file"):
        parser.read_csv(path)

