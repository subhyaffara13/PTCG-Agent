
def test_sympy__physics__quantum__fermion__FermionOp():
    from sympy.physics.quantum.fermion import FermionOp
    assert _test_args(FermionOp('c'))
    assert _test_args(FermionOp('c', False))

