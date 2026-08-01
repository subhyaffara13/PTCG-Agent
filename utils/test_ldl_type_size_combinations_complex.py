
def test_ldl_type_size_combinations_complex(n, dtype):
    rng = np.random.default_rng(1234)
    msg1 = (f"Her failed for size: {n}, dtype: {dtype}")
    msg2 = (f"Sym failed for size: {n}, dtype: {dtype}")

    # Complex hermitian upper/lower
    x = (rng.random((n, n))+1j*rng.random((n, n))).astype(dtype)
    x = x+x.conj().T
    x += eye(n, dtype=dtype)*dtype(rng.integers(5, 1e6))

    l, d1, p = ldl(x)
    u, d2, p = ldl(x, lower=0)
    rtol = 2e-4 if dtype is complex64 else 1e-10
    assert_allclose(l.dot(d1).dot(l.conj().T), x, rtol=rtol, err_msg=msg1)
    assert_allclose(u.dot(d2).dot(u.conj().T), x, rtol=rtol, err_msg=msg1)

    # Complex symmetric upper/lower
    x = (rng.random((n, n))+1j*rng.random((n, n))).astype(dtype)
    x = x+x.T
    x += eye(n, dtype=dtype)*dtype(rng.integers(5, 1e6))

    l, d1, p = ldl(x, hermitian=0)
    u, d2, p = ldl(x, lower=0, hermitian=0)
    assert_allclose(l.dot(d1).dot(l.T), x, rtol=rtol, err_msg=msg2)
    assert_allclose(u.dot(d2).dot(u.T), x, rtol=rtol, err_msg=msg2)

