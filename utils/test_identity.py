
def test_identity():
    with warns_deprecated_sympy():
        I = IdentityOperator()
        O = Operator('O')
        x = Symbol("x")
        three = sympify(3)

        assert isinstance(I, IdentityOperator)
        assert isinstance(I, Operator)

        assert I * O == O
        assert O * I == O
        assert I * Dagger(O) == Dagger(O)
        assert Dagger(O) * I == Dagger(O)
        assert isinstance(I * I, IdentityOperator)
        assert three * I == three
        assert I * x == x
        assert I.inv() == I
        assert Dagger(I) == I
        assert qapply(I * O) == O
        assert qapply(O * I) == O

        for n in [2, 3, 5]:
            assert represent(IdentityOperator(n)) == eye(n)


def test_identity():
    # We do not use xp here because identity always returns numpy arrays
    atol = 1e-12
    # Test single identity
    tf = RigidTransform.identity()
    xp_assert_close(tf.as_matrix(), np.eye(4), atol=atol)
    # Test multiple identities
    tf = RigidTransform.identity(5)
    xp_assert_close(tf.as_matrix(), np.array([np.eye(4)] * 5), atol=atol)
    # Test shape
    tf = RigidTransform.identity(shape=3)
    expected = np.tile(np.eye(4), (3, 1, 1))
    xp_assert_close(tf.as_matrix(), expected, atol=atol)
    tf = RigidTransform.identity(shape=(2, 3))
    expected = np.tile(np.eye(4), (2, 3, 1, 1))
    xp_assert_close(tf.as_matrix(), expected, atol=atol)
    # Test errors
    with pytest.raises(ValueError, match="Only one of `num` and `shape` can be."):
        RigidTransform.identity(10, shape=(2, 3))
    with pytest.raises(TypeError, match="takes from 0 to 1 positional arguments"):
        RigidTransform.identity(None, (-1, 3))  # Shape is kwarg only
    with pytest.raises(ValueError, match="`shape` must be an int or a tuple of ints"):
        RigidTransform.identity(shape="invalid")


def test_identity(xp):
    ident = interface.IdentityOperator((3, 3), xp=xp)
    xp_assert_equal(ident @ xp.asarray([1, 2, 3]), xp.asarray([1, 2, 3]))
    xp_assert_equal(xp_ravel(ident.dot(xp.reshape(xp.arange(9), (3, 3)))), xp.arange(9))

    assert_raises(ValueError, ident.matvec, xp.asarray([1, 2, 3, 4]))


def test_identity(klass, value):
    assert klass(value) is NaT


def test_identity():
    x = numpy.matlib.identity(2, dtype=int)
    assert_array_equal(x, np.matrix([[1, 0], [0, 1]]))


def test_identity(Poly):
    d = Poly.domain + random((2,)) * .25
    w = Poly.window + random((2,)) * .25
    x = np.linspace(d[0], d[1], 11)
    p = Poly.identity(domain=d, window=w)
    assert_equal(p.domain, d)
    assert_equal(p.window, w)
    assert_almost_equal(p(x), x)


def test_identity():
    p = poly.Polynomial.identity(domain=[-1, 1], window=[5, 20], symbol='z')
    assert_equal(p.symbol, 'z')

