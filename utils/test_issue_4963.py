
def test_issue_4963():
    assert hasattr(Mul(x, y), "is_commutative")
    assert hasattr(Mul(x, y, evaluate=False), "is_commutative")
    assert hasattr(Pow(x, y), "is_commutative")
    assert hasattr(Pow(x, y, evaluate=False), "is_commutative")
    expr = Mul(Pow(2, 2, evaluate=False), 3, evaluate=False) + 1
    assert hasattr(expr, "is_commutative")

