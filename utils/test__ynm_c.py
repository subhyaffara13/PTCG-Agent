
def test_Ynm_c():
    th, ph = Symbol("theta", real=True), Symbol("phi", real=True)
    from sympy.abc import n,m

    assert Ynm_c(n, m, th, ph) == (-1)**(2*m)*exp(-2*I*m*ph)*Ynm(n, m, th, ph)

