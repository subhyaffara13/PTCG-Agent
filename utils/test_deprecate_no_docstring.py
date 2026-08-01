
def test_deprecate_no_docstring():
    depr_func = deprecate(
        FutureWarning,
        "depr_func",
        new_func_no_docstring,
        "1.0",
        msg="Use new_func instead.",
    )
    with tm.assert_produces_warning(FutureWarning):
        result = depr_func()
    assert result == "new_func_no_docstring called"

