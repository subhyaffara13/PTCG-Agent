
def test_ldl_type_size_combinations_real(n, dtype):
    rng = np.random.default_rng(1234)
    msg = (f"Failed for size: {n}, dtype: {dtype}")

    x = rng.random((n, n)).astype(dtype)
    x = x + x.T
    x += eye(n, dtype=dtype)*dtype(rng.integers(5, 1e6))

    l, d1, p = ldl(x)
    u, d2, p = ldl(x, lower=0)
    rtol = 1e-4 if dtype is float32 else 1e-10
    assert_allclose(l.dot(d1).dot(l.T), x, rtol=rtol, err_msg=msg)
    assert_allclose(u.dot(d2).dot(u.T), x, rtol=rtol, err_msg=msg)

