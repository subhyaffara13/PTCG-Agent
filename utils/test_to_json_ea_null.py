
def test_to_json_ea_null():
    # GH#57224
    df = DataFrame(
        {
            "a": Series([1, NA], dtype="int64[pyarrow]"),
            "b": Series([2, NA], dtype="Int64"),
        }
    )
    result = df.to_json(orient="records", lines=True)
    expected = """{"a":1,"b":2}
{"a":null,"b":null}
"""
    assert result == expected

