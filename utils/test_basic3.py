
def test_basic3():
    assert limit(1/x, x, 0, dir="+") is oo
    assert limit(1/x, x, 0, dir="-") is -oo

