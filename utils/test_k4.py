
def test_K4():
    assert log(3 + 4*I).expand(complex=True) == log(5) + I*atan(R(4, 3))

