
def test_string_dtype_error_message():
    # GH#55051
    pytest.importorskip("pyarrow")
    msg = "Storage must be 'python' or 'pyarrow'."
    with pytest.raises(ValueError, match=msg):
        StringDtype("bla")

