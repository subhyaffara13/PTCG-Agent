
def test_mangle_cols_names(all_parsers, usecol, engine):
    # GH 11823
    parser = all_parsers
    data = "1,2,3"
    names = ["A", "A", "B"]
    with pytest.raises(ValueError, match="Duplicate names"):
        parser.read_csv(StringIO(data), names=names, usecols=usecol, engine=engine)

