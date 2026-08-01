
def test_due_date_enforcement(monkeypatch):
    class _MyDeprecation(SetuptoolsDeprecationWarning):
        _SUMMARY = "Summary"
        _DETAILS = "Lorem ipsum"
        _DUE_DATE = (2000, 11, 22)
        _SEE_DOCS = "some_page.html"

    monkeypatch.setenv("SETUPTOOLS_ENFORCE_DEPRECATION", "true")
    with pytest.raises(SetuptoolsDeprecationWarning) as exc_info:
        _MyDeprecation.emit()

    expected = """
    Summary
    !!

            ********************************************************************************
            Lorem ipsum

            This deprecation is overdue, please update your project and remove deprecated
            calls to avoid build errors in the future.

            See https://setuptools.pypa.io/en/latest/some_page.html for details.
            ********************************************************************************

    !!
    """
    assert str(exc_info.value) == cleandoc(expected)

