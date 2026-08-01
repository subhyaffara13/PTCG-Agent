
def assert_unitary(a, rtol=None, atol=None, assert_sqr=True):
    if rtol is None:
        rtol = 10.0 ** -(np.finfo(a.dtype).precision-2)
    if atol is None:
        atol = 10*np.finfo(a.dtype).eps

    if assert_sqr:
        assert_(a.shape[0] == a.shape[1], 'unitary matrices must be square')
    aTa = np.dot(a.T.conj(), a)
    assert_allclose(aTa, np.eye(a.shape[1]), rtol=rtol, atol=atol)

