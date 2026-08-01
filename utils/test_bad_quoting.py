
def test_bad_quoting(all_parsers, quoting, msg):
    data = "1,2,3"
    parser = all_parsers

    with pytest.raises(TypeError, match=msg):
        parser.read_csv(StringIO(data), quoting=quoting)

