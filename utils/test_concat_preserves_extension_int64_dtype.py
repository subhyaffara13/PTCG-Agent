
def test_concat_preserves_extension_int64_dtype():
    # GH 24768
    df_a = DataFrame({"a": [-1]}, dtype="Int64")
    df_b = DataFrame({"b": [1]}, dtype="Int64")
    result = concat([df_a, df_b], ignore_index=True)
    expected = DataFrame({"a": [-1, None], "b": [None, 1]}, dtype="Int64")
    tm.assert_frame_equal(result, expected)

