
def test_DifferentialOperatorEqPoly():
    x = symbols('x', integer=True)
    R, Dx = DifferentialOperators(QQ.old_poly_ring(x), 'Dx')
    do = DifferentialOperator([x**2, R.base.zero, R.base.zero], R)
    do2 = DifferentialOperator([x**2, 1, x], R)
    assert not do == do2

    # polynomial comparison issue, see https://github.com/sympy/sympy/pull/15799
    # should work once that is solved
    # p = do.listofpoly[0]
    # assert do == p

    p2 = do2.listofpoly[0]
    assert not do2 == p2

