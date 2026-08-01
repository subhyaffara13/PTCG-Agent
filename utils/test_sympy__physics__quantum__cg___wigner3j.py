
def test_sympy__physics__quantum__cg__Wigner3j():
    from sympy.physics.quantum.cg import Wigner3j
    assert _test_args(Wigner3j(6, 0, 4, 0, 2, 0))

