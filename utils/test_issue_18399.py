
def test_issue_18399():
    assert limit((1 - S(1)/2*x)**(3*x), x, oo) is zoo
    assert limit((-x)**x, x, oo) is zoo

