
def test_error_already_set_message_with_malformed_utf8():
    assert m.error_already_set_what(RuntimeError, b"\x80") == (
        "RuntimeError: b'\\x80'",
        False,
    )

