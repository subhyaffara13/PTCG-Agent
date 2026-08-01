
def check_form_qTu(q_order, q_shape, u_order, u_shape, u_ndim, dtype):
    rng = np.random.default_rng(47)
    if u_shape == 1 and u_ndim == 1:
        u_shape = (q_shape[0],)
    else:
        u_shape = (q_shape[0], u_shape)
    dtype = np.dtype(dtype)

    if dtype.char in 'fd':
        q = rng.random(q_shape)
        u = rng.random(u_shape)
    elif dtype.char in 'FD':
        q = rng.random(q_shape) + 1j*rng.random(q_shape)
        u = rng.random(u_shape) + 1j*rng.random(u_shape)
    else:
        raise ValueError("form_qTu doesn't support this dtype")

    q = np.require(q, dtype, q_order)
    if u_order != 'A':
        u = np.require(u, dtype, u_order)
    else:
        u, = make_strided((u.astype(dtype),))

    rtol = 10.0 ** -(np.finfo(dtype).precision-2)
    atol = 2*np.finfo(dtype).eps

    expected = np.dot(q.T.conj(), u)
    res = _decomp_update._form_qTu(q, u)
    assert_allclose(res, expected, rtol=rtol, atol=atol)

