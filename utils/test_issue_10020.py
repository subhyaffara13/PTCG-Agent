
def test_issue_10020():
    assert oo**I is S.NaN
    assert oo**(1 + I) is S.ComplexInfinity
    assert oo**(-1 + I) is S.Zero
    assert (-oo)**I is S.NaN
    assert (-oo)**(-1 + I) is S.Zero
    assert oo**t == Pow(oo, t, evaluate=False)
    assert (-oo)**t == Pow(-oo, t, evaluate=False)

