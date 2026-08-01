
def test_sympy__physics__secondquant__Commutator():
    from sympy.physics.secondquant import Commutator
    x, y = symbols('x y', commutative=False)
    assert _test_args(Commutator(x, y))

