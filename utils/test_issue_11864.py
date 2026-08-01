
def test_issue_11864():
    w, k = symbols('w, k', real=True)
    F = Piecewise((1, Eq(2*pi*k, 0)), (sin(pi*k)/(pi*k), True))
    soln = Piecewise((1, Eq(2*pi*k, 0)), (sinc(pi*k), True))
    assert F.rewrite(sinc) == soln

