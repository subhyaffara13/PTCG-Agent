
def test_to_jsonl():
    # GH9180
    df = DataFrame([[1, 2], [1, 2]], columns=["a", "b"])
    result = df.to_json(orient="records", lines=True)
    expected = '{"a":1,"b":2}\n{"a":1,"b":2}\n'
    assert result == expected

    df = DataFrame([["foo}", "bar"], ['foo"', "bar"]], columns=["a", "b"])
    result = df.to_json(orient="records", lines=True)
    expected = '{"a":"foo}","b":"bar"}\n{"a":"foo\\"","b":"bar"}\n'
    assert result == expected
    tm.assert_frame_equal(read_json(StringIO(result), lines=True), df)

    # GH15096: escaped characters in columns and data
    df = DataFrame([["foo\\", "bar"], ['foo"', "bar"]], columns=["a\\", "b"])
    result = df.to_json(orient="records", lines=True)
    expected = '{"a\\\\":"foo\\\\","b":"bar"}\n{"a\\\\":"foo\\"","b":"bar"}\n'
    assert result == expected
    tm.assert_frame_equal(read_json(StringIO(result), lines=True), df)

