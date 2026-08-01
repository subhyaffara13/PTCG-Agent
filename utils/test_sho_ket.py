
def test_SHOKet():
    assert SHOKet('k').dual_class() == SHOBra
    assert SHOBra('b').dual_class() == SHOKet
    assert InnerProduct(b,k).doit() == KroneckerDelta(k.n, b.n)
    assert k.hilbert_space == ComplexSpace(S.Infinity)
    assert k3_rep[k3.n, 0] == Integer(1)
    assert b3_rep[0, b3.n] == Integer(1)

