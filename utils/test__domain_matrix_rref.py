
def test_DomainMatrix_rref():
    # More tests in test_rref.py
    A = DomainMatrix([], (0, 1), QQ)
    assert A.rref() == (A, ())

    A = DomainMatrix([[QQ(1)]], (1, 1), QQ)
    assert A.rref() == (A, (0,))

    A = DomainMatrix([[QQ(0)]], (1, 1), QQ)
    assert A.rref() == (A, ())

    A = DomainMatrix([[QQ(1), QQ(2)], [QQ(3), QQ(4)]], (2, 2), QQ)
    Ar, pivots = A.rref()
    assert Ar == DomainMatrix([[QQ(1), QQ(0)], [QQ(0), QQ(1)]], (2, 2), QQ)
    assert pivots == (0, 1)

    A = DomainMatrix([[QQ(0), QQ(2)], [QQ(3), QQ(4)]], (2, 2), QQ)
    Ar, pivots = A.rref()
    assert Ar == DomainMatrix([[QQ(1), QQ(0)], [QQ(0), QQ(1)]], (2, 2), QQ)
    assert pivots == (0, 1)

    A = DomainMatrix([[QQ(0), QQ(2)], [QQ(0), QQ(4)]], (2, 2), QQ)
    Ar, pivots = A.rref()
    assert Ar == DomainMatrix([[QQ(0), QQ(1)], [QQ(0), QQ(0)]], (2, 2), QQ)
    assert pivots == (1,)

    Az = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    Ar, pivots = Az.rref()
    assert Ar == DomainMatrix([[QQ(1), QQ(0)], [QQ(0), QQ(1)]], (2, 2), QQ)
    assert pivots == (0, 1)

    methods = ('auto', 'GJ', 'FF', 'CD', 'GJ_dense', 'FF_dense', 'CD_dense')
    Az = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    for method in methods:
        Ar, pivots = Az.rref(method=method)
        assert Ar == DomainMatrix([[QQ(1), QQ(0)], [QQ(0), QQ(1)]], (2, 2), QQ)
        assert pivots == (0, 1)

    raises(ValueError, lambda: Az.rref(method='foo'))
    raises(ValueError, lambda: Az.rref_den(method='foo'))

