
def test_extract_expand_index_raises():
    # GH9980
    # Index only works with one regex group since
    # multi-group would expand to a frame
    idx = Index(["A1", "A2", "A3", "A4", "B5"])
    msg = "only one regex group is supported with Index"
    with pytest.raises(ValueError, match=msg):
        idx.str.extract("([AB])([123])", expand=False)

