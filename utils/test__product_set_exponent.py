
def test_ProductSet_exponent():
    ucode_str = '      1\n[0, 1] '
    assert upretty(Interval(0, 1)**1) == ucode_str
    ucode_str = '      2\n[0, 1] '
    assert upretty(Interval(0, 1)**2) == ucode_str

