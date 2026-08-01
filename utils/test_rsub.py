
def test_rsub(date, offset2):
    assert date - offset2 == (-offset2)._apply(date)

