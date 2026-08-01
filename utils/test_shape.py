
def test_shape():
    m = ShapingOnlyMatrix(1, 2, [0, 0])
    assert m.shape == (1, 2)


def test_shape():
    M = Matrix([[x, 0, 0],
                [0, y, 0]])
    assert M.shape == (2, 3)


def test_shape():
    m = Matrix(1, 2, [0, 0])
    assert m.shape == (1, 2)
    M = Matrix([[x, 0, 0],
                [0, y, 0]])
    assert M.shape == (2, 3)


def test_shape():
    c0, c1, c2 = symbols('c0:3')
    x = Symbol('x')
    assert CompanionMatrix(Poly([1, c0], x)).shape == (1, 1)
    assert CompanionMatrix(Poly([1, c1, c0], x)).shape == (2, 2)
    assert CompanionMatrix(Poly([1, c2, c1, c0], x)).shape == (3, 3)


def test_shape():
    B = MatrixSlice(X, (a, b), (c, d))
    assert B.shape == (b - a, d - c)


def test_shape():
    def f(x, arg):
        return x - arg

    for dt in [float, complex]:
        x = np.zeros([2,2])
        arg = np.ones([2,2], dtype=dt)

        sol = root(f, x, args=(arg,), method='DF-SANE')
        assert_(sol.success)
        assert_equal(sol.x.shape, x.shape)

