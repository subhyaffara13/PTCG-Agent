
def test_str_10000_digits():
    mp.dps = 10001
    # last digit may be wrong
    assert str(mpf(2)**0.5)[-10:-1] == '5873258351'[:9]
    assert str(pi)[-10:-1] == '5256375678'[:9]
    mp.dps = 15

