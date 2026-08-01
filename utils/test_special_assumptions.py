
def test_special_assumptions():
    e = -3 - sqrt(5) + (-sqrt(10)/2 - sqrt(2)/2)**2
    assert simplify(e < 0) is S.false
    assert simplify(e > 0) is S.false
    assert (e == 0) is False  # it's not a literal 0
    assert e.equals(0) is True

