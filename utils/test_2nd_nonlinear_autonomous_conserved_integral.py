
def test_2nd_nonlinear_autonomous_conserved_integral():
    eq = f(x).diff(x, 2) + asin(f(x))
    actual = [Eq(Integral(1/sqrt(C1 - 2*Integral(asin(_u), _u)), (_u, f(x))), C2 + x),
    Eq(Integral(1/sqrt(C1 - 2*Integral(asin(_u), _u)), (_u, f(x))), C2 - x)]
    solved = dsolve(eq, hint='2nd_nonlinear_autonomous_conserved_Integral', simplify=False)
    for a,s in zip(actual, solved):
        assert a.dummy_eq(s)
    # checkodesol unable to simplify solutions with f(x) in an integral equation
    assert checkodesol(eq, [s.doit() for s in solved]) == [(True, 0), (True, 0)]

