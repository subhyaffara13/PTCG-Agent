
def test_sympy__physics__quantum__density__Density():
    from sympy.physics.quantum.density import Density
    from sympy.physics.quantum.state import Ket
    assert _test_args(Density([Ket(0), 0.5], [Ket(1), 0.5]))

