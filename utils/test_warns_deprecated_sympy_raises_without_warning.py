
def test_warns_deprecated_sympy_raises_without_warning():
    with raises(Failed):
        with warns_deprecated_sympy():
            pass

