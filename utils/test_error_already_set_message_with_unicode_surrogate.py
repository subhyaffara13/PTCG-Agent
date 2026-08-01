
def test_error_already_set_message_with_unicode_surrogate():  # Issue #4288
    assert m.error_already_set_what(RuntimeError, "\ud927") == (
        "RuntimeError: \\ud927",
        False,
    )

