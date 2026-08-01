
def test_DomainScalar_repr():
    A = DomainScalar(ZZ(1), ZZ)
    assert repr(A) in {'1', 'mpz(1)'}

