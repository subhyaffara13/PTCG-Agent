
def test_PowerBasis_element__conversions():
    k = QQ.cyclotomic_field(5)
    L = QQ.cyclotomic_field(7)
    B = PowerBasis(k)

    # ANP --> PowerBasisElement
    a = k([QQ(1, 2), QQ(1, 3), 5, 7])
    e = B.element_from_ANP(a)
    assert e.coeffs == [42, 30, 2, 3]
    assert e.denom == 6

    # PowerBasisElement --> ANP
    assert e.to_ANP() == a

    # Cannot convert ANP from different field
    d = L([QQ(1, 2), QQ(1, 3), 5, 7])
    raises(UnificationFailed, lambda: B.element_from_ANP(d))

    # AlgebraicNumber --> PowerBasisElement
    alpha = k.to_alg_num(a)
    eps = B.element_from_alg_num(alpha)
    assert eps.coeffs == [42, 30, 2, 3]
    assert eps.denom == 6

    # PowerBasisElement --> AlgebraicNumber
    assert eps.to_alg_num() == alpha

    # Cannot convert AlgebraicNumber from different field
    delta = L.to_alg_num(d)
    raises(UnificationFailed, lambda: B.element_from_alg_num(delta))

    # When we don't know the field:
    C = PowerBasis(k.ext.minpoly)
    # Can convert from AlgebraicNumber:
    eps = C.element_from_alg_num(alpha)
    assert eps.coeffs == [42, 30, 2, 3]
    assert eps.denom == 6
    # But can't convert back:
    raises(StructureError, lambda: eps.to_alg_num())

