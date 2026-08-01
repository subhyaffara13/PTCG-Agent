
def test_literal_json_raises():
    # PR 53409
    jsonl = """{"a": 1, "b": 2}
        {"a": 3, "b": 4}
        {"a": 5, "b": 6}
        {"a": 7, "b": 8}"""

    msg = r".* does not exist"

    with pytest.raises(FileNotFoundError, match=msg):
        read_json(jsonl, lines=False)

    with pytest.raises(FileNotFoundError, match=msg):
        read_json('{"a": 1, "b": 2}\n{"b":2, "a" :1}\n', lines=True)

    with pytest.raises(FileNotFoundError, match=msg):
        read_json(
            '{"a\\\\":"foo\\\\","b":"bar"}\n{"a\\\\":"foo\\"","b":"bar"}\n',
            lines=False,
        )

    with pytest.raises(FileNotFoundError, match=msg):
        read_json('{"a": 1, "b": 2}\n{"b":2, "a" :1}\n', lines=False)

