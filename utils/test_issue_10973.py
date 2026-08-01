
def test_issue_10973():
    assert Sum((-n + (n**3 + 1)**(S(1)/3))/log(n), (n, 1, oo)).is_convergent() is S.true

