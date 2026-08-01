
def test_bool_eq():
    assert 0 == False
    assert S(0) == False
    assert S(0) != S.false
    assert 1 == True
    assert S.One == True
    assert S.One != S.true

