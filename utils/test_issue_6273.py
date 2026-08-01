
def test_issue_6273():
    assert Sum(x, (x, 1, n)).n(2, subs={n: 1}) == Float(1, 2)

