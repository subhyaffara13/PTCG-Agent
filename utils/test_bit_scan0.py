
def test_bit_scan0():
    assert bit_scan0(-1) is None
    assert bit_scan0(0) == 0
    assert bit_scan0(1) == 1
    assert bit_scan0(-2) == 0

