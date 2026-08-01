
def test_checked_call_with_bad_call(monkeypatch):
    """
    Give CheckCall a function that returns a falsey value and
    mock get_errno so it returns false so an exception is raised.
    """

    def _return_false():
        return False

    monkeypatch.setattr("pandas.io.clipboard.get_errno", lambda: True)
    msg = f"Error calling {_return_false.__name__} \\(Window Error\\)"

    with pytest.raises(PyperclipWindowsException, match=msg):
        CheckedCall(_return_false)()

