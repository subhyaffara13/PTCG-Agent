
def test_sympy__physics__quantum__cg__Wigner6j():
    from sympy.physics.quantum.cg import Wigner6j
    assert _test_args(Wigner6j(1, 2, 3, 2, 1, 2))

