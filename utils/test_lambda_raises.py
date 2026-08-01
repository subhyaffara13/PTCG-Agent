
def test_lambda_raises():
    raises(SympifyError, lambda: sympify("lambda *args: args")) # args argument error
    raises(SympifyError, lambda: sympify("lambda **kwargs: kwargs[0]")) # kwargs argument error
    raises(SympifyError, lambda: sympify("lambda x = 1: x"))    # Keyword argument error
    with raises(SympifyError):
        _sympify('lambda: 1')

