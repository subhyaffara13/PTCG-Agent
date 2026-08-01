
def test_diff_by_matrix():

    # Derive matrix by matrix:

    A = MutableDenseMatrix([[x, y], [z, t]])
    assert A.diff(A) == Array([[[[1, 0], [0, 0]], [[0, 1], [0, 0]]], [[[0, 0], [1, 0]], [[0, 0], [0, 1]]]])
    assert diff(A, A) == Array([[[[1, 0], [0, 0]], [[0, 1], [0, 0]]], [[[0, 0], [1, 0]], [[0, 0], [0, 1]]]])

    A_imm = A.as_immutable()
    assert A_imm.diff(A_imm) == Array([[[[1, 0], [0, 0]], [[0, 1], [0, 0]]], [[[0, 0], [1, 0]], [[0, 0], [0, 1]]]])
    assert diff(A_imm, A_imm) == Array([[[[1, 0], [0, 0]], [[0, 1], [0, 0]]], [[[0, 0], [1, 0]], [[0, 0], [0, 1]]]])

    # Derive a constant matrix:
    assert A.diff(a) == MutableDenseMatrix([[0, 0], [0, 0]])

    B = ImmutableDenseMatrix([a, b])
    assert A.diff(B) == Array.zeros(2, 1, 2, 2)
    assert A.diff(A) == Array([[[[1, 0], [0, 0]], [[0, 1], [0, 0]]], [[[0, 0], [1, 0]], [[0, 0], [0, 1]]]])

    # Test diff with tuples:

    dB = B.diff([[a, b]])
    assert dB.shape == (2, 2, 1)
    assert dB == Array([[[1], [0]], [[0], [1]]])

    f = Function("f")
    fxyz = f(x, y, z)
    assert fxyz.diff([[x, y, z]]) == Array([fxyz.diff(x), fxyz.diff(y), fxyz.diff(z)])
    assert fxyz.diff(([x, y, z], 2)) == Array([
        [fxyz.diff(x, 2), fxyz.diff(x, y), fxyz.diff(x, z)],
        [fxyz.diff(x, y), fxyz.diff(y, 2), fxyz.diff(y, z)],
        [fxyz.diff(x, z), fxyz.diff(z, y), fxyz.diff(z, 2)],
    ])

    expr = sin(x)*exp(y)
    assert expr.diff([[x, y]]) == Array([cos(x)*exp(y), sin(x)*exp(y)])
    assert expr.diff(y, ((x, y),)) == Array([cos(x)*exp(y), sin(x)*exp(y)])
    assert expr.diff(x, ((x, y),)) == Array([-sin(x)*exp(y), cos(x)*exp(y)])
    assert expr.diff(((y, x),), [[x, y]]) == Array([[cos(x)*exp(y), -sin(x)*exp(y)], [sin(x)*exp(y), cos(x)*exp(y)]])

    # Test different notations:

    assert fxyz.diff(x).diff(y).diff(x) == fxyz.diff(((x, y, z),), 3)[0, 1, 0]
    assert fxyz.diff(z).diff(y).diff(x) == fxyz.diff(((x, y, z),), 3)[2, 1, 0]
    assert fxyz.diff([[x, y, z]], ((z, y, x),)) == Array([[fxyz.diff(i).diff(j) for i in (x, y, z)] for j in (z, y, x)])

    # Test scalar derived by matrix remains matrix:
    res = x.diff(Matrix([[x, y]]))
    assert isinstance(res, ImmutableDenseMatrix)
    assert res == Matrix([[1, 0]])
    res = (x**3).diff(Matrix([[x, y]]))
    assert isinstance(res, ImmutableDenseMatrix)
    assert res == Matrix([[3*x**2, 0]])


def test_diff_by_matrix():

    # Derive matrix by matrix:

    A = MutableDenseMatrix([[x, y], [z, t]])
    assert A.diff(A) == Array([[[[1, 0], [0, 0]], [[0, 1], [0, 0]]], [[[0, 0], [1, 0]], [[0, 0], [0, 1]]]])
    assert diff(A, A) == Array([[[[1, 0], [0, 0]], [[0, 1], [0, 0]]], [[[0, 0], [1, 0]], [[0, 0], [0, 1]]]])

    A_imm = A.as_immutable()
    assert A_imm.diff(A_imm) == Array([[[[1, 0], [0, 0]], [[0, 1], [0, 0]]], [[[0, 0], [1, 0]], [[0, 0], [0, 1]]]])
    assert diff(A_imm, A_imm) == Array([[[[1, 0], [0, 0]], [[0, 1], [0, 0]]], [[[0, 0], [1, 0]], [[0, 0], [0, 1]]]])

    # Derive a constant matrix:
    assert A.diff(a) == MutableDenseMatrix([[0, 0], [0, 0]])

    B = ImmutableDenseMatrix([a, b])
    assert A.diff(B) == Array.zeros(2, 1, 2, 2)
    assert A.diff(A) == Array([[[[1, 0], [0, 0]], [[0, 1], [0, 0]]], [[[0, 0], [1, 0]], [[0, 0], [0, 1]]]])

    # Test diff with tuples:

    dB = B.diff([[a, b]])
    assert dB.shape == (2, 2, 1)
    assert dB == Array([[[1], [0]], [[0], [1]]])

    f = Function("f")
    fxyz = f(x, y, z)
    assert fxyz.diff([[x, y, z]]) == Array([fxyz.diff(x), fxyz.diff(y), fxyz.diff(z)])
    assert fxyz.diff(([x, y, z], 2)) == Array([
        [fxyz.diff(x, 2), fxyz.diff(x, y), fxyz.diff(x, z)],
        [fxyz.diff(x, y), fxyz.diff(y, 2), fxyz.diff(y, z)],
        [fxyz.diff(x, z), fxyz.diff(z, y), fxyz.diff(z, 2)],
    ])

    expr = sin(x)*exp(y)
    assert expr.diff([[x, y]]) == Array([cos(x)*exp(y), sin(x)*exp(y)])
    assert expr.diff(y, ((x, y),)) == Array([cos(x)*exp(y), sin(x)*exp(y)])
    assert expr.diff(x, ((x, y),)) == Array([-sin(x)*exp(y), cos(x)*exp(y)])
    assert expr.diff(((y, x),), [[x, y]]) == Array([[cos(x)*exp(y), -sin(x)*exp(y)], [sin(x)*exp(y), cos(x)*exp(y)]])

    # Test different notations:

    assert fxyz.diff(x).diff(y).diff(x) == fxyz.diff(((x, y, z),), 3)[0, 1, 0]
    assert fxyz.diff(z).diff(y).diff(x) == fxyz.diff(((x, y, z),), 3)[2, 1, 0]
    assert fxyz.diff([[x, y, z]], ((z, y, x),)) == Array([[fxyz.diff(i).diff(j) for i in (x, y, z)] for j in (z, y, x)])

    # Test scalar derived by matrix remains matrix:
    res = x.diff(Matrix([[x, y]]))
    assert isinstance(res, ImmutableDenseMatrix)
    assert res == Matrix([[1, 0]])
    res = (x**3).diff(Matrix([[x, y]]))
    assert isinstance(res, ImmutableDenseMatrix)
    assert res == Matrix([[3*x**2, 0]])

