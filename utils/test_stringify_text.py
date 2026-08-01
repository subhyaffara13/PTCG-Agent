
def test_stringify_text(text):
    valid_types = (str, int, float, bool)

    if isinstance(text, valid_types):
        result = _stringifyText(text)
        assert result == str(text)
    else:
        msg = (
            "only str, int, float, and bool values "
            f"can be copied to the clipboard, not {type(text).__name__}"
        )
        with pytest.raises(PyperclipException, match=msg):
            _stringifyText(text)

