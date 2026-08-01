
def test_warns_deprecated_sympy_wrong_stacklevel():
    with raises(Failed):
        with warns_deprecated_sympy():
            _warn_sympy_deprecation(stacklevel=1)

