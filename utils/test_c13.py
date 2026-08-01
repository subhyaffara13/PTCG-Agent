
def test_C13():
    test = R(10, 7) * (1 + R(29, 1000)) ** R(1, 3)
    good = 3 ** R(1, 3)
    assert test == good

