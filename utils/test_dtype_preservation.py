
def test_dtype_preservation(method, dtype):
    rtol = np.finfo(dtype).eps ** 0.75 * 100
    if method is FloaterHormannInterpolator:
        rtol *= 100
    rng = np.random.default_rng(59846294526092468)

    z = np.linspace(-1, 1, dtype=dtype)
    r = method(z, np.sin(z))

    z2 = rng.uniform(-1, 1, size=100).astype(dtype)
    assert_allclose(r(z2), np.sin(z2), rtol=rtol)
    assert r(z2).dtype == dtype

    if method is AAA:
        assert r.support_points.dtype == dtype
        assert r.support_values.dtype == dtype
        assert r.errors.dtype == z.real.dtype
    assert r.weights.dtype == dtype
    assert r.poles().dtype == np.result_type(dtype, 1j)
    assert r.residues().dtype == np.result_type(dtype, 1j)
    assert r.roots().dtype == np.result_type(dtype, 1j)

