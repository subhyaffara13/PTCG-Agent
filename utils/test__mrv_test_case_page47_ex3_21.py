
def test_MrvTestCase_page47_ex3_21():
    h = exp(-x/(1 + exp(-x)))
    expr = exp(h)*exp(-x/(1 + h))*exp(exp(-x + h))/h**2 - exp(x) + x
    assert mmrv(expr, x) == {1/h, exp(-x), exp(x), exp(x - h), exp(x/(1 + h))}

