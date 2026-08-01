
def test_sympy__physics__quantum__sho1d__Hamiltonian():
    from sympy.physics.quantum.sho1d import Hamiltonian
    assert _test_args(Hamiltonian('H'))

