
def test_invhyperb_inaccuracy():
    mp.dps = 15
    assert (asinh(1e-5)*10**5).ae(0.99999999998333333)
    assert (asinh(1e-10)*10**10).ae(1)
    assert (asinh(1e-50)*10**50).ae(1)
    assert (asinh(-1e-5)*10**5).ae(-0.99999999998333333)
    assert (asinh(-1e-10)*10**10).ae(-1)
    assert (asinh(-1e-50)*10**50).ae(-1)
    assert asinh(10**20).ae(46.744849040440862)
    assert asinh(-10**20).ae(-46.744849040440862)
    assert (tanh(1e-10)*10**10).ae(1)
    assert (tanh(-1e-10)*10**10).ae(-1)
    assert (atanh(1e-10)*10**10).ae(1)
    assert (atanh(-1e-10)*10**10).ae(-1)

