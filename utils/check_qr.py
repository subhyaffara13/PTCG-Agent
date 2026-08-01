
def check_qr(q, r, a, rtol, atol, assert_sqr=True):
    assert_unitary(q, rtol, atol, assert_sqr)
    assert_upper_tri(r, rtol, atol)
    assert_allclose(q.dot(r), a, rtol=rtol, atol=atol)

