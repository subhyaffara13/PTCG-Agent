
def test_sum():
    if not np:
        skip("NumPy not installed")

    s = Sum(x ** i, (i, a, b))
    f = lambdify((a, b, x), s, 'numpy')

    a_, b_ = 0, 10
    x_ = np.linspace(-1, +1, 10)
    assert np.allclose(f(a_, b_, x_), sum(x_ ** i_ for i_ in range(a_, b_ + 1)))

    s = Sum(i * x, (i, a, b))
    f = lambdify((a, b, x), s, 'numpy')

    a_, b_ = 0, 10
    x_ = np.linspace(-1, +1, 10)
    assert np.allclose(f(a_, b_, x_), sum(i_ * x_ for i_ in range(a_, b_ + 1)))


def test_sum():
    m = Matrix([[1, 2, 3], [x, y, x], [2*y, -50, z*x]])
    assert m + m == Matrix([[2, 4, 6], [2*x, 2*y, 2*x], [4*y, -100, 2*z*x]])
    n = Matrix(1, 2, [1, 2])
    raises(ShapeError, lambda: m + n)


def test_sum():
    m = Matrix([[1, 2, 3], [x, y, x], [2*y, -50, z*x]])
    assert m + m == Matrix([[2, 4, 6], [2*x, 2*y, 2*x], [4*y, -100, 2*z*x]])
    n = Matrix(1, 2, [1, 2])
    raises(ShapeError, lambda: m + n)


def test_sum(A):
    assert not isinstance(A.sum(axis=0), np.matrix), \
        "Expected array, got matrix"
    assert A.sum(axis=0).shape == (4,)
    assert A.sum(axis=1).shape == (3,)


def test_sum(shape, axis, out):
    rng = np.random.default_rng(23409823)
    a = random_array(shape, density=0.6, random_state=rng, dtype=int)

    res = a.sum(axis=axis, out=out)
    exp = np.sum(a.toarray(), axis=axis)
    assert_equal(res, exp)
    if out is not None:
        assert_equal(out, exp)
        assert id(res) == id(out)

