
def test_fht_special_cases(xp):
    rng = np.random.RandomState(3491349965)

    a = xp.asarray(rng.standard_normal(64))
    dln = rng.uniform(-1, 1)

    # let x = (mu+1+q)/2, y = (mu+1-q)/2, M = {0, -1, -2, ...}

    # case 1: x in M, y in M => well-defined transform
    mu, bias = -4.0, 1.0
    with warnings.catch_warnings(record=True) as record:
        fht(a, dln, mu, bias=bias)
        assert not record, 'fht warned about a well-defined transform'

    # case 2: x not in M, y in M => well-defined transform
    mu, bias = -2.5, 0.5
    with warnings.catch_warnings(record=True) as record:
        fht(a, dln, mu, bias=bias)
        assert not record, 'fht warned about a well-defined transform'

    # with fht_lock:
    # case 3: x in M, y not in M => singular transform
    mu, bias = -3.5, 0.5
    with pytest.warns(Warning) as record:
        fht(a, dln, mu, bias=bias)
        assert record, 'fht did not warn about a singular transform'

    # with fht_lock:
    # case 4: x not in M, y in M => singular inverse transform
    mu, bias = -2.5, 0.5
    with pytest.warns(Warning) as record:
        ifht(a, dln, mu, bias=bias)
        assert record, 'ifht did not warn about a singular transform'

