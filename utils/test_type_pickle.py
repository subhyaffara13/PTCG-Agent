
def test_type_pickle():
    # can't actually unpickle, but we can pickle (if in namespace)
    import pickle

    np._ScaledFloatTestDType = SF

    s = pickle.dumps(SF)
    res = pickle.loads(s)
    assert res is SF

    del np._ScaledFloatTestDType

