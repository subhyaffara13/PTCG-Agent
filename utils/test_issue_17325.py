
def test_issue_17325():
    assert Limit(sin(x)/x, x, 0, dir="+-").doit() == 1
    assert Limit(x**2, x, 0, dir="+-").doit() == 0
    assert Limit(1/x**2, x, 0, dir="+-").doit() is oo
    assert Limit(1/x, x, 0, dir="+-").doit() is zoo

