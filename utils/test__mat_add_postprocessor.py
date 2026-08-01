
def test_MatAdd_postprocessor():
    # Some of these are nonsensical, but we do not raise errors for Add
    # because that breaks algorithms that want to replace matrices with dummy
    # symbols.

    z = zeros(2)

    assert Add(0, z) == Add(z, 0) == z

    a = Add(S.Infinity, z)
    assert a == Add(z, S.Infinity)
    assert isinstance(a, Add)
    assert a.args == (S.Infinity, z)

    a = Add(S.ComplexInfinity, z)
    assert a == Add(z, S.ComplexInfinity)
    assert isinstance(a, Add)
    assert a.args == (S.ComplexInfinity, z)

    a = Add(z, S.NaN)
    # assert a == Add(S.NaN, z) # See the XFAIL above
    assert isinstance(a, Add)
    assert a.args == (S.NaN, z)

    M = Matrix([[1, 2], [3, 4]])
    a = Add(x, M)
    assert a == Add(M, x)
    assert isinstance(a, Add)
    assert a.args == (x, M)

    A = MatrixSymbol("A", 2, 2)
    assert Add(A, M) == Add(M, A) == A + M

    # Scalars should be absorbed into constant matrices (producing an error)
    a = Add(x, M, A)
    assert a == Add(M, x, A) == Add(M, A, x) == Add(x, A, M) == Add(A, x, M) == Add(A, M, x)
    assert isinstance(a, Add)
    assert a.args == (x, A + M)

    assert Add(M, M) == 2*M
    assert Add(M, A, M) == Add(M, M, A) == Add(A, M, M) == A + 2*M

    a = Add(A, x, M, M, x)
    assert isinstance(a, Add)
    assert a.args == (2*x, A + 2*M)

