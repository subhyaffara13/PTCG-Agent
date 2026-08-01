
def test_issue_14392():
    assert (sin(zoo)**2).as_real_imag() == (nan, nan)

