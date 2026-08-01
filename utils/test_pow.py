
def test_pow():
    if not np:
        skip('NumPy not installed')

    expr = Pow(2, -1, evaluate=False)
    f = lambdify([], expr, 'numpy')
    assert f() == 0.5


def test_pow():
    assert h**l == h**x == 1
    assert l**h == x**h == 2
    assert (x**l).args == (1/x).args and (x**l).is_Pow
    assert (l**x).args == ((-1)**x).args and (l**x).is_Pow


def test_pow(xp, ndim: int):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-6
    num = 10
    rng = np.random.default_rng(100)
    shape = (num,) + (ndim,) * (ndim - 1)
    t = xp.asarray(rng.normal(size=shape + (3,)), dtype=dtype)
    q = xp.asarray(rng.normal(size=shape + (4,)), dtype=dtype)
    r = Rotation.from_quat(q)
    p = RigidTransform.from_components(t, r)
    p_inv = p.inv()

    # Test the short-cuts and other integers
    for n in [-5, -2, -1, 0, 1, 2, 5]:
        q = p**n
        # Regression test for gh-24436
        assert isinstance(q._matrix, type(p._matrix))
        r = RigidTransform.from_matrix(xp.tile(xp.eye(4), shape + (1, 1)))
        for _ in range(abs(n)):
            if n > 0:
                r = r * p
            else:
                r = r * p_inv
        xp_assert_close(q.as_matrix(), r.as_matrix(), atol=atol)

    # Test shape preservation of single
    single_tf = RigidTransform.identity()
    assert (single_tf**n).as_matrix().shape == (4, 4)

    # Test fractional powers
    q = p**0.5
    xp_assert_close((q * q).as_matrix(), p.as_matrix(), atol=atol)
    q = p**-0.5
    xp_assert_close((q * q).as_matrix(), p.inv().as_matrix(), atol=atol)
    q = p** 1.5
    xp_assert_close((q * q).as_matrix(), (p**3).as_matrix(), atol=atol)
    q = p** -1.5
    xp_assert_close((q * q).as_matrix(), (p**-3).as_matrix(), atol=atol)

    # pow function
    tf = pow(RigidTransform.from_matrix(xp.eye(4)), 2)
    xp_assert_close(tf.as_matrix(), xp.eye(4), atol=atol)


def test_pow(xp, ndim: int):
    dtype = xpx.default_dtype(xp)
    atol = 1e-14 if dtype == xp.float64 else 1e-6
    rng = np.random.default_rng(0)
    batch_shape = (ndim,) * (ndim - 1)
    quat = rng.normal(size=batch_shape + (4,))
    p = Rotation.from_quat(xp.asarray(quat))
    p_inv = p.inv()
    # Test the short-cuts and other integers
    for n in [-5, -2, -1, 0, 1, 2, 5]:
        # Test accuracy
        q = p ** n
        q_identity = xp.asarray([0., 0, 0, 1])
        # Regression test for gh-24436 
        assert isinstance(q._quat, type(q_identity))
        r = Rotation.from_quat(xp.tile(q_identity, batch_shape + (1,)))
        for _ in range(abs(n)):
            if n > 0:
                r = r * p
            else:
                r = r * p_inv
        ang = (q * r.inv()).magnitude()
        assert xp.all(ang < atol)

        # Test shape preservation
        r = Rotation.from_quat(xp.tile(q_identity, batch_shape + (1,)))
        assert (r**n).as_quat().shape == batch_shape + (4,)

    # Large angle fractional
    for n in [-1.5, -0.5, -0.0, 0.0, 0.5, 1.5]:
        q = p ** n
        r = Rotation.from_rotvec(n * p.as_rotvec())
        xp_assert_close(q.as_quat(), r.as_quat(), atol=atol)

    # Array exponent
    n = [-5, -2, -1.5, -1, -0.5, -0.0, 0, 0.0, 0.5, 1.0, 1.5, 2]
    for exponent in n:
        r = p ** exponent
        r_array = p ** xp.asarray([exponent])  # Test with 1D array
        xp_assert_close(r.as_quat(), r_array.as_quat())
        r_array = p ** xp.asarray(exponent)  # Test with scalar
        xp_assert_close(r.as_quat(), r_array.as_quat())

    # Small angle
    rotvec = xp.zeros(batch_shape + (3,))
    rotvec = xpx.at(rotvec)[..., 0].set(1e-12)
    p = Rotation.from_rotvec(rotvec)
    n = 3
    q = p ** n
    r = Rotation.from_rotvec(n * p.as_rotvec())
    xp_assert_close(q.as_quat(), r.as_quat(), atol=atol)

    # Array exponent
    q = p ** xp.asarray([n])  # Test with 1D array
    r = Rotation.from_rotvec(n * p.as_rotvec())
    xp_assert_close(q.as_quat(), r.as_quat(), atol=atol)
    q = p ** xp.asarray(n)  # Test with scalar
    r = Rotation.from_rotvec(n * p.as_rotvec())
    xp_assert_close(q.as_quat(), r.as_quat(), atol=atol)


def test_pow(Poly):
    d = Poly.domain + random((2,)) * .25
    w = Poly.window + random((2,)) * .25
    tgt = Poly([1], domain=d, window=w)
    tst = Poly([1, 2, 3], domain=d, window=w)
    for i in range(5):
        assert_poly_almost_equal(tst**i, tgt)
        tgt = tgt * tst
    # default domain and window
    tgt = Poly([1])
    tst = Poly([1, 2, 3])
    for i in range(5):
        assert_poly_almost_equal(tst**i, tgt)
        tgt = tgt * tst
    # check error for invalid powers
    assert_raises(ValueError, op.pow, tgt, 1.5)
    assert_raises(ValueError, op.pow, tgt, -1)


def test_pow():
    assert mpf(6) ** mpf(3) == 216.0
    assert mpf(6) ** 3 == 216.0
    assert mpf(6) ** 3.0 == 216.0
    assert 6 ** mpf(3) == 216.0
    assert 6.0 ** mpf(3) == 216.0
    assert (6+0j) ** mpf(3.0) == 216.0
    assert mpc(6) ** mpf(3) == 216.0
    assert mpc(6) ** 3 == 216.0
    assert mpc(6) ** 3.0 == 216.0
    assert mpc(6) ** (3+0j) == 216.0
    assert 6 ** mpc(3) == 216.0
    assert 6.0 ** mpc(3) == 216.0
    assert (6+0j) ** mpc(3) == 216.0

