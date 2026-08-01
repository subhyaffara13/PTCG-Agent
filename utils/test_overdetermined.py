
def test_overdetermined():
    x = symbols('x', real=True)
    eqs = [Abs(4*x - 7) - 5, Abs(3 - 8*x) - 1]
    assert solve(eqs, x) == [(S.Half,)]
    assert solve(eqs, x, manual=True) == [(S.Half,)]
    assert solve(eqs, x, manual=True, check=False) == [(S.Half,), (S(3),)]

