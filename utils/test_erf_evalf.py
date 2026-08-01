
def test_erf_evalf():
    assert abs( erf(Float(2.0)) - 0.995322265 ) < 1E-8 # XXX

