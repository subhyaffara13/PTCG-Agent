
def test_unitroots():
    assert unitroots(1) == [1]
    assert unitroots(2) == [1, -1]
    a, b, c = unitroots(3)
    assert a == 1
    assert b.ae(-0.5 + 0.86602540378443864676j)
    assert c.ae(-0.5 - 0.86602540378443864676j)
    assert unitroots(1, primitive=True) == [1]
    assert unitroots(2, primitive=True) == [-1]
    assert unitroots(3, primitive=True) == unitroots(3)[1:]
    assert unitroots(4, primitive=True) == [j, -j]
    assert len(unitroots(17, primitive=True)) == 16
    assert len(unitroots(16, primitive=True)) == 8

