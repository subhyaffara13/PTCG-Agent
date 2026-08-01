
def test_dtype_backend_string(all_parsers, string_storage):
    # GH#36712
    with pd.option_context("mode.string_storage", string_storage):
        parser = all_parsers

        data = """a,b
a,x
b,
"""
        result = parser.read_csv(StringIO(data), dtype_backend="numpy_nullable")

        expected = DataFrame(
            {
                "a": pd.array(["a", "b"], dtype=pd.StringDtype(string_storage)),
                "b": pd.array(["x", pd.NA], dtype=pd.StringDtype(string_storage)),
            },
        )
    tm.assert_frame_equal(result, expected)

