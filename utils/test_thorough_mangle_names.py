
def test_thorough_mangle_names(all_parsers, data, names, expected):
    # see gh-17095
    parser = all_parsers

    with pytest.raises(ValueError, match="Duplicate names"):
        parser.read_csv(StringIO(data), names=names)

