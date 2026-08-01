
def test_derivative_subs3():
    dex = Derivative(exp(x), x)
    assert Derivative(dex, x).subs(dex, exp(x)) == dex
    assert dex.subs(exp(x), dex) == Derivative(exp(x), x, x)

