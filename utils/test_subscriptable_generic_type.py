
def test_subscriptable_generic_type():
    assert isinstance(ShortTimeFFT[np.float64], GenericAlias)

