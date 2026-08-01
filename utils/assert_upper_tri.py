
def assert_upper_tri(a, rtol=None, atol=None):
    if rtol is None:
        rtol = 10.0 ** -(np.finfo(a.dtype).precision-2)
    if atol is None:
        atol = 2*np.finfo(a.dtype).eps
    mask = np.tri(a.shape[0], a.shape[1], -1, np.bool_)
    assert_allclose(a[mask], 0.0, rtol=rtol, atol=atol)

