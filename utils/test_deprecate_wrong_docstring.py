
def test_deprecate_wrong_docstring():
    msg = "deprecate needs a correctly formatted docstring"
    with pytest.raises(AssertionError, match=msg):
        deprecate(
            FutureWarning,
            "depr_func",
            new_func_wrong_docstring,
            "1.0",
            msg="Use new_func instead.",
        )

