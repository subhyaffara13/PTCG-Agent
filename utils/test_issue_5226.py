
def test_issue_5226():
    assert Add(evaluate=False) == 0
    assert Mul(evaluate=False) == 1
    assert Mul(x + y, evaluate=False).is_Add

