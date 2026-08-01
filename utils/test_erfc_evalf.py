
def test_erfc_evalf():
    assert abs( erfc(Float(2.0)) - 0.00467773 ) < 1E-8 # XXX

