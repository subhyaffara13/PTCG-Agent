
def test_issue_14111():
    assert Sum(1/log(log(n)), (n, 22, oo)).is_convergent() is S.false

