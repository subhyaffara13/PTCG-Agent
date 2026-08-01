
def test_warns_deprecated_sympy_continues_after_warning():
    with warnings.catch_warnings(record=True) as w:
        finished = False
        with warns_deprecated_sympy():
            _warn_sympy_deprecation()
            finished = True
        assert finished
        assert len(w) == 0

