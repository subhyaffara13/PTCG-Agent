
def test_sympy__physics__quantum__cg__CG():
    from sympy.physics.quantum.cg import CG
    from sympy.core.singleton import S
    assert _test_args(CG(Rational(3, 2), Rational(3, 2), S.Half, Rational(-1, 2), 1, 1))

