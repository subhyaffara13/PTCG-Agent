
def test_readjson_nrows_requires_lines(engine):
    # GH 33916
    # Test ValueError raised if nrows is set without setting lines in read_json
    jsonl = """{"a": 1, "b": 2}
        {"a": 3, "b": 4}
        {"a": 5, "b": 6}
        {"a": 7, "b": 8}"""
    msg = "nrows can only be passed if lines=True"
    with pytest.raises(ValueError, match=msg):
        read_json(jsonl, lines=False, nrows=2, engine=engine)

