
def test_issue_17556():
    z = I*oo
    assert z.is_imaginary is False
    assert z.is_finite is False

