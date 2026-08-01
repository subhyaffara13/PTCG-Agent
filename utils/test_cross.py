
def test_cross():
    v1 = C.x * i + C.z * C.z * j
    v2 = C.x * i + C.y * j + C.z * k
    assert Cross(v1, v2) == Cross(C.x*C.i + C.z**2*C.j, C.x*C.i + C.y*C.j + C.z*C.k)
    assert Cross(v1, v2).doit() == C.z**3*C.i + (-C.x*C.z)*C.j + (C.x*C.y - C.x*C.z**2)*C.k
    assert cross(v1, v2) == C.z**3*C.i + (-C.x*C.z)*C.j + (C.x*C.y - C.x*C.z**2)*C.k
    assert Cross(v1, v2) == -Cross(v2, v1)
    # XXX: Cannot use Cross here. See XFAIL test below:
    assert cross(v1, v2) + cross(v2, v1) == Vector.zero


def test_cross():
    assert cross(A.x, A.x) == 0
    assert cross(A.x, A.y) == A.z
    assert cross(A.x, A.z) == -A.y

    assert cross(A.y, A.x) == -A.z
    assert cross(A.y, A.y) == 0
    assert cross(A.y, A.z) == A.x

    assert cross(A.z, A.x) == A.y
    assert cross(A.z, A.y) == -A.x
    assert cross(A.z, A.z) == 0


def test_cross():
    a = [1, 2, 3]
    b = [3, 4, 5]
    col = Matrix([-2, 4, -2])
    row = col.T

    def test(M, ans):
        assert ans == M
        assert type(M) == cls
    for cls in classes:
        A = cls(a)
        B = cls(b)
        test(A.cross(B), col)
        test(A.cross(B.T), col)
        test(A.T.cross(B.T), row)
        test(A.T.cross(B), row)
    raises(ShapeError, lambda:
        Matrix(1, 2, [1, 1]).cross(Matrix(1, 2, [1, 1])))


def test_cross():
    a = [1, 2, 3]
    b = [3, 4, 5]
    col = Matrix([-2, 4, -2])
    row = col.T

    def test(M, ans):
        assert ans == M
        assert type(M) == cls
    for cls in all_classes:
        A = cls(a)
        B = cls(b)
        test(A.cross(B), col)
        test(A.cross(B.T), col)
        test(A.T.cross(B.T), row)
        test(A.T.cross(B), row)
    raises(ShapeError, lambda:
        Matrix(1, 2, [1, 1]).cross(Matrix(1, 2, [1, 1])))


def test_cross():
    x = np.arange(9).reshape((3, 3))
    actual = np.linalg.cross(x, x + 1)
    expected = np.array([
        [-1, 2, -1],
        [-1, 2, -1],
        [-1, 2, -1],
    ])

    assert_equal(actual, expected)

    # We test that lists are converted to arrays.
    u = [1, 2, 3]
    v = [4, 5, 6]
    actual = np.linalg.cross(u, v)
    expected = array([-3,  6, -3])

    assert_equal(actual, expected)

    with assert_raises_regex(
        ValueError,
        r"input arrays must be \(arrays of\) 3-dimensional vectors"
    ):
        x_2dim = x[:, 1:]
        np.linalg.cross(x_2dim, x_2dim)

