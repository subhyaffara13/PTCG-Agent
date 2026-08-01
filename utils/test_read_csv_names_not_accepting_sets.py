
def test_read_csv_names_not_accepting_sets(all_parsers):
    # GH 34946
    data = """\
    1,2,3
    4,5,6\n"""
    parser = all_parsers
    with pytest.raises(ValueError, match="Names should be an ordered collection."):
        parser.read_csv(StringIO(data), names=set("QAZ"))

