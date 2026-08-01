
def test_pow_equivalence_with_rotation(xp, ndim: int):
    atol = 1e-12
    num = 10
    rng = np.random.default_rng(100)
    dtype = xpx.default_dtype(xp)
    shape = (num,) + (ndim,) * (ndim - 1)

    r = Rotation.from_quat(xp.asarray(rng.normal(size=shape + (4,)), dtype=dtype))
    p = RigidTransform.from_rotation(r)
    for n in [-5, -2, -1.5, -1, -0.5, 0.0, 0.5, 1, 1.5, 2, 5]:
        xp_assert_close((p**n).rotation.as_matrix(), (r**n).as_matrix(), atol=atol)

