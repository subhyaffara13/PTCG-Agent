
def test_ProductSet_is_empty():
    assert ProductSet(S.Integers, S.Reals).is_empty == False
    assert ProductSet(Interval(x, 1), S.Reals).is_empty == None

