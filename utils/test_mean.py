
def test_mean(xp, ndim: int):
    atol = 1e-12
    rng = np.random.default_rng(123)

    dtype = xpx.default_dtype(xp)
    t = xp.asarray(rng.normal(size=(ndim,) * (ndim - 1) + (3,)), dtype=dtype)
    q = xp.asarray(rng.normal(size=(ndim,) * (ndim - 1) + (4,)), dtype=dtype)
    r = Rotation.from_quat(q)
    tf = RigidTransform.from_components(t, r)

    # Unweighted mean
    axis = tuple(range(t.ndim - 1))
    t_mean = xp.mean(t, axis=axis)
    r_mean = r.mean()
    tf_mean = tf.mean()
    assert tf_mean.shape == ()
    xp_assert_close(tf_mean.as_matrix(),
                    RigidTransform.from_components(t_mean, r_mean).as_matrix(),
                    atol=atol)

    # Weighted mean
    if ndim == 1:
        weights = None
        t_mean = t
    else:
        weights = xp.asarray(rng.random(size=(ndim,) * (ndim - 1)), dtype=dtype)
        norm = xp.sum(weights[..., None], axis=axis)
        wsum = xp.sum(t * weights[..., None], axis=axis)
        t_mean = wsum/norm
    r_mean = r.mean(weights=weights)
    tf_mean = tf.mean(weights=weights)
    assert tf_mean.shape == ()
    xp_assert_close(tf_mean.as_matrix(),
                    RigidTransform.from_components(t_mean, r_mean).as_matrix(),
                    atol=atol)


def test_mean(xp, ndim: int):
    axes = xp.concat((-xp.eye(3), xp.eye(3)))
    axes = xp.reshape(axes, (1,) * (ndim - 1) + (6, 3))
    thetas = xp.linspace(0, xp.pi / 2, 100)
    desired = xp.asarray(0.0)[()]
    atol = 1e-6 if xp_default_dtype(xp) is xp.float32 else 1e-10
    for t in thetas:
        r_mean = Rotation.from_rotvec(t * axes).mean()
        assert r_mean.shape == ()
        xp_assert_close(r_mean.magnitude(), desired, atol=atol)


def test_mean(A):
    assert not isinstance(A.mean(axis=1), np.matrix), \
        "Expected array, got matrix"


def test_mean(shape, axis, out):
    rng = np.random.default_rng(23409823)
    a = random_array(shape, density=0.6, random_state=rng, dtype=int)

    res = a.mean(axis=axis, out=out)
    exp = np.mean(a.toarray(), axis=axis)
    assert_allclose(res, exp)
    if out is not None:
        assert id(res) == id(out)
        assert_allclose(out, exp)

