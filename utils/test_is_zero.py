
def test_is_zero():
    assert PropertiesOnlyMatrix(0, 0, []).is_zero_matrix
    assert PropertiesOnlyMatrix([[0, 0], [0, 0]]).is_zero_matrix
    assert PropertiesOnlyMatrix(zeros(3, 4)).is_zero_matrix
    assert not PropertiesOnlyMatrix(eye(3)).is_zero_matrix
    assert PropertiesOnlyMatrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert PropertiesOnlyMatrix([[x, 1], [0, 0]]).is_zero_matrix == False
    a = Symbol('a', nonzero=True)
    assert PropertiesOnlyMatrix([[a, 0], [0, 0]]).is_zero_matrix == False


def test_is_zero():
    assert Matrix().is_zero_matrix
    assert Matrix([[0, 0], [0, 0]]).is_zero_matrix
    assert zeros(3, 4).is_zero_matrix
    assert not eye(3).is_zero_matrix
    assert Matrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert SparseMatrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert ImmutableMatrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert ImmutableSparseMatrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert Matrix([[x, 1], [0, 0]]).is_zero_matrix == False
    a = Symbol('a', nonzero=True)
    assert Matrix([[a, 0], [0, 0]]).is_zero_matrix == False


def test_is_zero():
    assert Matrix().is_zero_matrix
    assert Matrix([[0, 0], [0, 0]]).is_zero_matrix
    assert zeros(3, 4).is_zero_matrix
    assert not eye(3).is_zero_matrix
    assert Matrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert SparseMatrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert ImmutableMatrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert ImmutableSparseMatrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert Matrix([[x, 1], [0, 0]]).is_zero_matrix == False
    a = Symbol('a', nonzero=True)
    assert Matrix([[a, 0], [0, 0]]).is_zero_matrix == False


def test_is_zero():
    from sympy.abc import x, m
    assert Integral(0, (x, 1, x)).is_zero
    assert Integral(1, (x, 1, 1)).is_zero
    assert Integral(1, (x, 1, 2), (y, 2)).is_zero is False
    assert Integral(x, (m, 0)).is_zero
    assert Integral(x + m, (m, 0)).is_zero is None
    i = Integral(m, (m, 1, exp(x)), (x, 0))
    assert i.is_zero is None
    assert Integral(m, (x, 0), (m, 1, exp(x))).is_zero is True

    assert Integral(x, (x, oo, oo)).is_zero # issue 8171
    assert Integral(x, (x, -oo, -oo)).is_zero

    # this is zero but is beyond the scope of what is_zero
    # should be doing
    assert Integral(sin(x), (x, 0, 2*pi)).is_zero is None


def test_is_zero():
    for func in [Sum, Product]:
        assert func(0, (x, 1, 1)).is_zero is True
        assert func(x, (x, 1, 1)).is_zero is None

    assert Sum(0, (x, 1, 0)).is_zero is True
    assert Product(0, (x, 1, 0)).is_zero is False

