
def test_issue_3825():
    """catch: hash instability"""
    x = Symbol("x")
    y = Symbol("y")
    a1 = x + y
    a2 = y + x
    a2.is_comparable

    h1 = hash(a1)
    h2 = hash(a2)
    assert h1 == h2

