
def test_DomainMatrix_nullspace():
    A = DomainMatrix([[QQ(1), QQ(1)], [QQ(1), QQ(1)]], (2, 2), QQ)
    Anull = DomainMatrix([[QQ(-1), QQ(1)]], (1, 2), QQ)
    assert A.nullspace() == Anull

    A = DomainMatrix([[ZZ(1), ZZ(1)], [ZZ(1), ZZ(1)]], (2, 2), ZZ)
    Anull = DomainMatrix([[ZZ(-1), ZZ(1)]], (1, 2), ZZ)
    assert A.nullspace() == Anull

    raises(DMNotAField, lambda: A.nullspace(divide_last=True))

    A = DomainMatrix([[ZZ(2), ZZ(2)], [ZZ(2), ZZ(2)]], (2, 2), ZZ)
    Anull = DomainMatrix([[ZZ(-2), ZZ(2)]], (1, 2), ZZ)

    Arref, den, pivots = A.rref_den()
    assert den == ZZ(2)
    assert Arref.nullspace_from_rref() == Anull
    assert Arref.nullspace_from_rref(pivots) == Anull
    assert Arref.to_sparse().nullspace_from_rref() == Anull.to_sparse()
    assert Arref.to_sparse().nullspace_from_rref(pivots) == Anull.to_sparse()

