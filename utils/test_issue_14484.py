
def test_issue_14484():
    assert Sum(sin(n)/log(log(n)), (n, 22, oo)).is_convergent() is S.false

