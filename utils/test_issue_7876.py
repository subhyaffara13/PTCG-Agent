
def test_issue_7876():
    l1 = Poly(x**6 - x + 1, x).all_roots()
    l2 = [rootof(x**6 - x + 1, i) for i in range(6)]
    assert frozenset(l1) == frozenset(l2)

