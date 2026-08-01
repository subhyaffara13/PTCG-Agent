
def test_astype_to_string_dtype_not_modifying_input(any_string_dtype, val):
    # GH#51073 - variant of the above test with explicit dtype instances
    df = DataFrame({"a": ["a", "b", val]})
    expected = df.copy()
    df.astype(any_string_dtype)
    tm.assert_frame_equal(df, expected)

