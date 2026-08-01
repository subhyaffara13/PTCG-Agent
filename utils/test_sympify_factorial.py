
def test_sympify_factorial():
    assert sympify('x!') == factorial(x)
    assert sympify('(x+1)!') == factorial(x + 1)
    assert sympify('(1 + y*(x + 1))!') == factorial(1 + y*(x + 1))
    assert sympify('(1 + y*(x + 1)!)^2') == (1 + y*factorial(x + 1))**2
    assert sympify('y*x!') == y*factorial(x)
    assert sympify('x!!') == factorial2(x)
    assert sympify('(x+1)!!') == factorial2(x + 1)
    assert sympify('(1 + y*(x + 1))!!') == factorial2(1 + y*(x + 1))
    assert sympify('(1 + y*(x + 1)!!)^2') == (1 + y*factorial2(x + 1))**2
    assert sympify('y*x!!') == y*factorial2(x)
    assert sympify('factorial2(x)!') == factorial(factorial2(x))

    raises(SympifyError, lambda: sympify("+!!"))
    raises(SympifyError, lambda: sympify(")!!"))
    raises(SympifyError, lambda: sympify("!"))
    raises(SympifyError, lambda: sympify("(!)"))
    raises(SympifyError, lambda: sympify("x!!!"))

