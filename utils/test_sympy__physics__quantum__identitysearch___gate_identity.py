
def test_sympy__physics__quantum__identitysearch__GateIdentity():
    from sympy.physics.quantum.gate import X
    from sympy.physics.quantum.identitysearch import GateIdentity
    assert _test_args(GateIdentity(X(0), X(0)))

