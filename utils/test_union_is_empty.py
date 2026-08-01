
def test_union_is_empty():
    assert (Interval(x, y) + FiniteSet(1)).is_empty == False
    assert (Interval(x, y) + Interval(-x, y)).is_empty == None

