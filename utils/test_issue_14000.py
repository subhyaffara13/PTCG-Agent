
def test_issue_14000():
    assert isinstance(sqrt(4, evaluate=False), Pow) == True
    assert isinstance(cbrt(3.5, evaluate=False), Pow) == True
    assert isinstance(root(16, 4, evaluate=False), Pow) == True

    assert sqrt(4, evaluate=False) == Pow(4, S.Half, evaluate=False)
    assert cbrt(3.5, evaluate=False) == Pow(3.5, Rational(1, 3), evaluate=False)
    assert root(4, 2, evaluate=False) == Pow(4, S.Half, evaluate=False)

    assert root(16, 4, 2, evaluate=False).has(Pow) == True
    assert real_root(-8, 3, evaluate=False).has(Pow) == True

