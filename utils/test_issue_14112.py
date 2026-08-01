
def test_issue_14112():
    assert Sum((-1)**n/sqrt(n), (n, 1, oo)).is_absolutely_convergent() is S.false
    assert Sum((-1)**(2*n)/n, (n, 1, oo)).is_convergent() is S.false
    assert Sum((-2)**n + (-3)**n, (n, 1, oo)).is_convergent() is S.false

