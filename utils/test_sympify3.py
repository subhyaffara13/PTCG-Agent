
def test_sympify3():
    assert sympify("x**3") == x**3
    assert sympify("x^3") == x**3
    assert sympify("1/2") == Integer(1)/2

    raises(SympifyError, lambda: _sympify('x**3'))
    raises(SympifyError, lambda: _sympify('1/2'))

