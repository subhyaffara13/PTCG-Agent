
def test_subscriptable_generic_types(cls):
    assert isinstance(cls[np.float64], GenericAlias)

