
def test_sympy__physics__quantum__commutator__Commutator():
    from sympy.physics.quantum.commutator import Commutator
    A, B = symbols('A,B', commutative=False)
    assert _test_args(Commutator(A, B))

