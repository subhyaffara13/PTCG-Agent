
def test_dataframe_to_arrow(using_infer_string):
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["a", "b", "c"]})

    table = pa.RecordBatchReader.from_stream(df).read_all()
    string_type = pa.large_string() if using_infer_string else pa.string()
    expected = pa.table({"a": [1, 2, 3], "b": pa.array(["a", "b", "c"], string_type)})
    assert table.equals(expected)

    schema = pa.schema([("a", pa.int8()), ("b", pa.string())])
    table = pa.RecordBatchReader.from_stream(df, schema=schema).read_all()
    expected = expected.cast(schema)
    assert table.equals(expected)

