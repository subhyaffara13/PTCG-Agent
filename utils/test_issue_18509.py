
def test_issue_18509():
    x = Symbol('x', prime=True)
    assert x**oo is oo
    assert (1/x)**oo is S.Zero
    assert (-1/x)**oo is S.Zero
    assert (-x)**oo is zoo
    assert (-oo)**(-1 + I) is S.Zero
    assert (-oo)**(1 + I) is zoo
    assert (oo)**(-1 + I) is S.Zero
    assert (oo)**(1 + I) is zoo

