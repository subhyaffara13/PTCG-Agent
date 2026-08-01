
def test_integer_promotion(method, dtype):
    z = np.arange(10, dtype=dtype)
    r = method(z, z)
    assert r.weights.dtype == np.result_type(dtype, 1.0)
    if method is AAA:
        assert r.support_points.dtype == np.result_type(dtype, 1.0)
        assert r.support_values.dtype == np.result_type(dtype, 1.0)
        assert r.errors.dtype == np.result_type(dtype, 1.0)
    assert r.poles().dtype == np.result_type(dtype, 1j)
    assert r.residues().dtype == np.result_type(dtype, 1j)
    assert r.roots().dtype == np.result_type(dtype, 1j)

    assert r(z).dtype == np.result_type(dtype, 1.0)

