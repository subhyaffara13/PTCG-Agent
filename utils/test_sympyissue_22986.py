
def test_sympyissue_22986():
    assert limit(acosh(1 + 1/x)*sqrt(x), x, oo) == sqrt(2)

