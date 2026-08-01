
def test_richcompare_scalar_boolean_singleton_return():
    # These are currently guaranteed to be the boolean numpy singletons
    assert (np.array(0) == "a") is np.bool_(False)
    assert (np.array(0) != "a") is np.bool_(True)
    assert (np.int16(0) == "a") is np.bool_(False)
    assert (np.int16(0) != "a") is np.bool_(True)

