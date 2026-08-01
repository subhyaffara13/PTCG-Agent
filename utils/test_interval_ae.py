
def test_interval_ae():
    iv.dps = 15
    x = iv.mpf([1,2])
    assert x.ae(1) is None
    assert x.ae(1.5) is None
    assert x.ae(2) is None
    assert x.ae(2.01) is False
    assert x.ae(0.99) is False
    x = iv.mpf(3.5)
    assert x.ae(3.5) is True
    assert x.ae(3.5+1e-15) is True
    assert x.ae(3.5-1e-15) is True
    assert x.ae(3.501) is False
    assert x.ae(3.499) is False
    assert x.ae(iv.mpf([3.5,3.501])) is None
    assert x.ae(iv.mpf([3.5,4.5+1e-15])) is None

