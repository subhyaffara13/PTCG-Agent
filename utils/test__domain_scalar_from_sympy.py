
def test_DomainScalar_from_sympy():
    expr = S(1)
    B = DomainScalar.from_sympy(expr)
    assert B == DomainScalar(ZZ(1), ZZ)

