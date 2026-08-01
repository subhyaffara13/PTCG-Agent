
def test_from_sequence_of_strings_boolean():
    true_strings = ["true", "TRUE", "True", "1", "1.0"]
    false_strings = ["false", "FALSE", "False", "0", "0.0"]
    nulls = [None]
    strings = true_strings + false_strings + nulls
    bools = (
        [True] * len(true_strings) + [False] * len(false_strings) + [None] * len(nulls)
    )

    dtype = ArrowDtype(pa.bool_())
    result = ArrowExtensionArray._from_sequence_of_strings(strings, dtype=dtype)
    expected = pd.array(bools, dtype="boolean[pyarrow]")
    tm.assert_extension_array_equal(result, expected)

    strings = ["True", "foo"]
    with pytest.raises(pa.ArrowInvalid, match="Failed to parse"):
        ArrowExtensionArray._from_sequence_of_strings(strings, dtype=dtype)

