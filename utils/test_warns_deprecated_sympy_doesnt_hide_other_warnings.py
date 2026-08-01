
def test_warns_deprecated_sympy_doesnt_hide_other_warnings():
    # Unlike pytest's deprecated_call, we should not hide other warnings.
    with raises(RuntimeWarning):
        with warns_deprecated_sympy():
            _warn_sympy_deprecation()
            warnings.warn('this is the other message', RuntimeWarning)

