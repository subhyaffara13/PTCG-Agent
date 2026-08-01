
def test_diag_make():
    diag = SpecialOnlyMatrix.diag
    a = Matrix([[1, 2], [2, 3]])
    b = Matrix([[3, x], [y, 3]])
    c = Matrix([[3, x, 3], [y, 3, z], [x, y, z]])
    assert diag(a, b, b) == Matrix([
        [1, 2, 0, 0, 0, 0],
        [2, 3, 0, 0, 0, 0],
        [0, 0, 3, x, 0, 0],
        [0, 0, y, 3, 0, 0],
        [0, 0, 0, 0, 3, x],
        [0, 0, 0, 0, y, 3],
    ])
    assert diag(a, b, c) == Matrix([
        [1, 2, 0, 0, 0, 0, 0],
        [2, 3, 0, 0, 0, 0, 0],
        [0, 0, 3, x, 0, 0, 0],
        [0, 0, y, 3, 0, 0, 0],
        [0, 0, 0, 0, 3, x, 3],
        [0, 0, 0, 0, y, 3, z],
        [0, 0, 0, 0, x, y, z],
    ])
    assert diag(a, c, b) == Matrix([
        [1, 2, 0, 0, 0, 0, 0],
        [2, 3, 0, 0, 0, 0, 0],
        [0, 0, 3, x, 3, 0, 0],
        [0, 0, y, 3, z, 0, 0],
        [0, 0, x, y, z, 0, 0],
        [0, 0, 0, 0, 0, 3, x],
        [0, 0, 0, 0, 0, y, 3],
    ])
    a = Matrix([x, y, z])
    b = Matrix([[1, 2], [3, 4]])
    c = Matrix([[5, 6]])
    # this "wandering diagonal" is what makes this
    # a block diagonal where each block is independent
    # of the others
    assert diag(a, 7, b, c) == Matrix([
        [x, 0, 0, 0, 0, 0],
        [y, 0, 0, 0, 0, 0],
        [z, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 0, 0],
        [0, 0, 1, 2, 0, 0],
        [0, 0, 3, 4, 0, 0],
        [0, 0, 0, 0, 5, 6]])
    raises(ValueError, lambda: diag(a, 7, b, c, rows=5))
    assert diag(1) == Matrix([[1]])
    assert diag(1, rows=2) == Matrix([[1, 0], [0, 0]])
    assert diag(1, cols=2) == Matrix([[1, 0], [0, 0]])
    assert diag(1, rows=3, cols=2) == Matrix([[1, 0], [0, 0], [0, 0]])
    assert diag(*[2, 3]) == Matrix([
        [2, 0],
        [0, 3]])
    assert diag(Matrix([2, 3])) == Matrix([
        [2],
        [3]])
    assert diag([1, [2, 3], 4], unpack=False) == \
            diag([[1], [2, 3], [4]], unpack=False) == Matrix([
        [1, 0],
        [2, 3],
        [4, 0]])
    assert type(diag(1)) == SpecialOnlyMatrix
    assert type(diag(1, cls=Matrix)) == Matrix
    assert Matrix.diag([1, 2, 3]) == Matrix.diag(1, 2, 3)
    assert Matrix.diag([1, 2, 3], unpack=False).shape == (3, 1)
    assert Matrix.diag([[1, 2, 3]]).shape == (3, 1)
    assert Matrix.diag([[1, 2, 3]], unpack=False).shape == (1, 3)
    assert Matrix.diag([[[1, 2, 3]]]).shape == (1, 3)
    # kerning can be used to move the starting point
    assert Matrix.diag(ones(0, 2), 1, 2) == Matrix([
        [0, 0, 1, 0],
        [0, 0, 0, 2]])
    assert Matrix.diag(ones(2, 0), 1, 2) == Matrix([
        [0, 0],
        [0, 0],
        [1, 0],
        [0, 2]])


def test_diag_make():
    diag = Matrix.diag
    a = Matrix([[1, 2], [2, 3]])
    b = Matrix([[3, x], [y, 3]])
    c = Matrix([[3, x, 3], [y, 3, z], [x, y, z]])
    assert diag(a, b, b) == Matrix([
        [1, 2, 0, 0, 0, 0],
        [2, 3, 0, 0, 0, 0],
        [0, 0, 3, x, 0, 0],
        [0, 0, y, 3, 0, 0],
        [0, 0, 0, 0, 3, x],
        [0, 0, 0, 0, y, 3],
    ])
    assert diag(a, b, c) == Matrix([
        [1, 2, 0, 0, 0, 0, 0],
        [2, 3, 0, 0, 0, 0, 0],
        [0, 0, 3, x, 0, 0, 0],
        [0, 0, y, 3, 0, 0, 0],
        [0, 0, 0, 0, 3, x, 3],
        [0, 0, 0, 0, y, 3, z],
        [0, 0, 0, 0, x, y, z],
    ])
    assert diag(a, c, b) == Matrix([
        [1, 2, 0, 0, 0, 0, 0],
        [2, 3, 0, 0, 0, 0, 0],
        [0, 0, 3, x, 3, 0, 0],
        [0, 0, y, 3, z, 0, 0],
        [0, 0, x, y, z, 0, 0],
        [0, 0, 0, 0, 0, 3, x],
        [0, 0, 0, 0, 0, y, 3],
    ])
    a = Matrix([x, y, z])
    b = Matrix([[1, 2], [3, 4]])
    c = Matrix([[5, 6]])
    # this "wandering diagonal" is what makes this
    # a block diagonal where each block is independent
    # of the others
    assert diag(a, 7, b, c) == Matrix([
        [x, 0, 0, 0, 0, 0],
        [y, 0, 0, 0, 0, 0],
        [z, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 0, 0],
        [0, 0, 1, 2, 0, 0],
        [0, 0, 3, 4, 0, 0],
        [0, 0, 0, 0, 5, 6]])
    raises(ValueError, lambda: diag(a, 7, b, c, rows=5))
    assert diag(1) == Matrix([[1]])
    assert diag(1, rows=2) == Matrix([[1, 0], [0, 0]])
    assert diag(1, cols=2) == Matrix([[1, 0], [0, 0]])
    assert diag(1, rows=3, cols=2) == Matrix([[1, 0], [0, 0], [0, 0]])
    assert diag(*[2, 3]) == Matrix([
        [2, 0],
        [0, 3]])
    assert diag(Matrix([2, 3])) == Matrix([
        [2],
        [3]])
    assert diag([1, [2, 3], 4], unpack=False) == \
            diag([[1], [2, 3], [4]], unpack=False) == Matrix([
        [1, 0],
        [2, 3],
        [4, 0]])
    assert type(diag(1)) == Matrix
    assert type(diag(1, cls=Matrix)) == Matrix
    assert Matrix.diag([1, 2, 3]) == Matrix.diag(1, 2, 3)
    assert Matrix.diag([1, 2, 3], unpack=False).shape == (3, 1)
    assert Matrix.diag([[1, 2, 3]]).shape == (3, 1)
    assert Matrix.diag([[1, 2, 3]], unpack=False).shape == (1, 3)
    assert Matrix.diag([[[1, 2, 3]]]).shape == (1, 3)
    # kerning can be used to move the starting point
    assert Matrix.diag(ones(0, 2), 1, 2) == Matrix([
        [0, 0, 1, 0],
        [0, 0, 0, 2]])
    assert Matrix.diag(ones(2, 0), 1, 2) == Matrix([
        [0, 0],
        [0, 0],
        [1, 0],
        [0, 2]])

