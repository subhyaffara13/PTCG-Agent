
def test_erfi_evalf():
    assert abs( erfi(Float(2.0)) - 18.5648024145756 ) < 1E-13  # XXX

