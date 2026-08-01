
def test_issue_18442():
    assert limit(tan(x)**(2**(sqrt(pi))), x, oo, dir='-') == Limit(tan(x)**(2**(sqrt(pi))), x, oo, dir='-')

