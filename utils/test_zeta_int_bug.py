
def test_zeta_int_bug():
    assert mpf_zeta_int(0, 10) == from_float(-0.5)

