
def test_DomainScalar_to_sympy():
    B = DomainScalar(ZZ(1), ZZ)
    expr = B.to_sympy()
    assert expr.is_Integer and expr == 1

