
def test_roundtrip_zero_dimensions():
    stream = BytesIO()
    savemat(stream, {'d':np.empty((10, 0))})
    d = loadmat(stream)
    assert d['d'].shape == (10, 0)

