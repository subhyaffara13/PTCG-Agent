
def test_warns_deprecated_sympy_catches_warning():
    with warnings.catch_warnings(record=True) as w:
        with warns_deprecated_sympy():
            _warn_sympy_deprecation()
        assert len(w) == 0

