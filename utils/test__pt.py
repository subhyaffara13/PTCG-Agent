
def test__pt():
    from sympy.solvers.inequalities import _pt
    assert _pt(-oo, oo) == 0
    assert _pt(S.One, S(3)) == 2
    assert _pt(S.One, oo) == _pt(oo, S.One) == 2
    assert _pt(S.One, -oo) == _pt(-oo, S.One) == S.Half
    assert _pt(S.NegativeOne, oo) == _pt(oo, S.NegativeOne) == Rational(-1, 2)
    assert _pt(S.NegativeOne, -oo) == _pt(-oo, S.NegativeOne) == -2
    assert _pt(x, oo) == _pt(oo, x) == x + 1
    assert _pt(x, -oo) == _pt(-oo, x) == x - 1
    raises(ValueError, lambda: _pt(Dummy('i', infinite=True), S.One))

