
def test_cossin(dtype_, m, p, q, swap_sign):
    rng = default_rng(1708093570726217)
    if dtype_ in COMPLEX_DTYPES:
        x = np.array(unitary_group.rvs(m, random_state=rng), dtype=dtype_)
    else:
        x = np.array(ortho_group.rvs(m, random_state=rng), dtype=dtype_)

    u, cs, vh = cossin(x, p, q,
                       swap_sign=swap_sign)
    assert_allclose(x, u @ cs @ vh, rtol=0., atol=m*1e3*np.finfo(dtype_).eps)
    assert u.dtype == dtype_
    # Test for float32 or float 64
    assert cs.dtype == np.real(u).dtype
    assert vh.dtype == dtype_

    u, cs, vh = cossin([x[:p, :q], x[:p, q:], x[p:, :q], x[p:, q:]],
                       swap_sign=swap_sign)
    assert_allclose(x, u @ cs @ vh, rtol=0., atol=m*1e3*np.finfo(dtype_).eps)
    assert u.dtype == dtype_
    assert cs.dtype == np.real(u).dtype
    assert vh.dtype == dtype_

    _, cs2, vh2 = cossin(x, p, q,
                         compute_u=False,
                         swap_sign=swap_sign)
    assert_allclose(cs, cs2, rtol=0., atol=10*np.finfo(dtype_).eps)
    assert_allclose(vh, vh2, rtol=0., atol=10*np.finfo(dtype_).eps)

    u2, cs2, _ = cossin(x, p, q,
                        compute_vh=False,
                        swap_sign=swap_sign)
    assert_allclose(u, u2, rtol=0., atol=10*np.finfo(dtype_).eps)
    assert_allclose(cs, cs2, rtol=0., atol=10*np.finfo(dtype_).eps)

    _, cs2, _ = cossin(x, p, q,
                       compute_u=False,
                       compute_vh=False,
                       swap_sign=swap_sign)
    assert_allclose(cs, cs2, rtol=0., atol=10*np.finfo(dtype_).eps)

