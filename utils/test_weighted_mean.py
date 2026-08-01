
def test_weighted_mean(xp, ndim: int):
    # test that doubling a weight is equivalent to including a rotation twice.
    thetas = xp.linspace(0, xp.pi / 2, 100)

    # Create batched copies of the same setup
    batch_shape = (ndim,) * (ndim - 1)
    axes = xp.asarray([[0.0, 0, 0], [1, 0, 0], [1, 0, 0]])
    weights = xp.asarray([1, 2])
    axes = xp.tile(axes, batch_shape + (1, 1))
    weights = xp.tile(weights, batch_shape + (1,))

    expected = xp.asarray(0.0)[()]
    for t in thetas:
        rw = Rotation.from_rotvec(t * axes[..., :2, :])
        mw = rw.mean(weights=weights)

        r = Rotation.from_rotvec(t * axes)
        m = r.mean()
        assert m.shape == ()
        xp_assert_close((m * mw.inv()).magnitude(), expected, atol=1e-6)

