
def test_Div_By_Zero():
    assert 1/S.Zero is zoo
    assert 1/Float(0) is zoo
    assert 0/S.Zero is nan
    assert 0/Float(0) is nan
    assert S.Zero/0 is nan
    assert Float(0)/0 is nan
    assert -1/S.Zero is zoo
    assert -1/Float(0) is zoo

