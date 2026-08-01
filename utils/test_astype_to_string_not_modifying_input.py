
def test_astype_to_string_not_modifying_input(string_storage, val):
    # GH#51073
    df = DataFrame({"a": ["a", "b", val]})
    expected = df.copy()
    with option_context("mode.string_storage", string_storage):
        df.astype("string")
    tm.assert_frame_equal(df, expected)

