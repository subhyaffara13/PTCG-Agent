
def test_Matrix_to_DM():

    M = Matrix([[1, 2], [3, 4]])
    assert M.to_DM() == DMs([[1, 2], [3, 4]], ZZ)
    assert M.to_DM() is not M._rep
    assert M.to_DM(field=True) == DMs([[1, 2], [3, 4]], QQ)
    assert M.to_DM(domain=QQ) == DMs([[1, 2], [3, 4]], QQ)
    assert M.to_DM(domain=QQ[x]) == DMs([[1, 2], [3, 4]], QQ[x])
    assert M.to_DM(domain=GF(3)) == DMs([[1, 2], [0, 1]], GF(3))

    M = Matrix([[1, 2], [3, 4]])
    M[0, 0] = x
    assert M._rep.domain == EXRAW
    M[0, 0] = 1
    assert M.to_DM() == DMs([[1, 2], [3, 4]], ZZ)

    M = Matrix([[S(1)/2, 2], [3, 4]])
    assert M.to_DM() == DMs([[QQ(1,2), 2], [3, 4]], QQ)

    M = Matrix([[x, 2], [3, 4]])
    assert M.to_DM() == DMs([[x, 2], [3, 4]], ZZ[x])
    assert M.to_DM(field=True) == DMs([[x, 2], [3, 4]], ZZ.frac_field(x))

    M = Matrix([[1/x, 2], [3, 4]])
    assert M.to_DM() == DMs([[1/x, 2], [3, 4]], ZZ.frac_field(x))

    M = Matrix([[1, sqrt(2)], [3, 4]])
    K = QQ.algebraic_field(sqrt(2))
    sqrt2 = K.from_sympy(sqrt(2)) # XXX: Maybe K(sqrt(2)) should work
    M_K = DomainMatrix([[K(1), sqrt2], [K(3), K(4)]], (2, 2), K)
    assert M.to_DM() == DMs([[1, sqrt(2)], [3, 4]], EXRAW)
    assert M.to_DM(extension=True) == M_K.to_sparse()

    # Options cannot be used with the domain parameter
    M = Matrix([[1, 2], [3, 4]])
    raises(TypeError, lambda: M.to_DM(domain=QQ, field=True))

