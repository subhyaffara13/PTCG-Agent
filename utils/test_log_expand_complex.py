
def test_log_expand_complex():
    assert log(1 + I).expand(complex=True) == log(2)/2 + I*pi/4
    assert log(1 - sqrt(2)).expand(complex=True) == log(sqrt(2) - 1) + I*pi

