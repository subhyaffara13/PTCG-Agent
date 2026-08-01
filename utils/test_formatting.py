
def test_formatting():
    S = Logic.fromstring
    raises(ValueError, lambda: S('a&b'))
    raises(ValueError, lambda: S('a|b'))
    raises(ValueError, lambda: S('! a'))


def test_formatting(monkeypatch, example_name):
    """
    It should automatically handle indentation, interpolation and things like due date.
    """
    args = _EXAMPLES[example_name]["args"]
    kwargs = _EXAMPLES[example_name]["kwargs"]
    expected = _EXAMPLES[example_name]["expected"]

    monkeypatch.setenv("SETUPTOOLS_ENFORCE_DEPRECATION", "false")
    with pytest.warns(SetuptoolsWarning) as warn_info:
        SetuptoolsWarning.emit(*args, **kwargs)
    assert _get_message(warn_info) == cleandoc(expected)

