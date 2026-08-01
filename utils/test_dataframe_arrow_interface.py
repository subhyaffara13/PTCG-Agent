
def test_dataframe_arrow_interface(using_infer_string):
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["a", "b", "c"]})

    capsule = df.__arrow_c_stream__()
    assert (
        ctypes.pythonapi.PyCapsule_IsValid(
            ctypes.py_object(capsule), b"arrow_array_stream"
        )
        == 1
    )

    table = pa.table(df)
    string_type = pa.large_string() if using_infer_string else pa.string()
    expected = pa.table({"a": [1, 2, 3], "b": pa.array(["a", "b", "c"], string_type)})
    assert table.equals(expected)

    schema = pa.schema([("a", pa.int8()), ("b", pa.string())])
    table = pa.table(df, schema=schema)
    expected = expected.cast(schema)
    assert table.equals(expected)

