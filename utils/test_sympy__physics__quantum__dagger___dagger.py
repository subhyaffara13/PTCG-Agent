
def test_sympy__physics__quantum__dagger__Dagger():
    from sympy.physics.quantum.dagger import Dagger
    from sympy.physics.quantum.state import Ket
    assert _test_args(Dagger(Dagger(Ket('psi'))))

