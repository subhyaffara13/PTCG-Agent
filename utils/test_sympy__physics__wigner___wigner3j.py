
def test_sympy__physics__wigner__Wigner3j():
    from sympy.physics.wigner import Wigner3j
    assert _test_args(Wigner3j(0, 0, 0, 0, 0, 0))

