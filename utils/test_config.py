
def test_config(string_storage):
    # with the default string_storage setting
    # always "python" at the moment
    assert StringDtype().storage == "pyarrow" if HAS_PYARROW else "python"

    with pd.option_context("string_storage", string_storage):
        assert StringDtype().storage == string_storage
        result = pd.array(["a", "b"])
        assert result.dtype.storage == string_storage

    # pd.array(..) by default always returns the NA-variant
    dtype = StringDtype(string_storage, na_value=pd.NA)
    expected = dtype.construct_array_type()._from_sequence(["a", "b"], dtype=dtype)
    tm.assert_equal(result, expected)

