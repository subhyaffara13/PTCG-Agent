
def test_issue_21031():
    assert limit(((1 + x)**(1/x) - (1 + 2*x)**(1/(2*x)))/asin(x), x, 0) == E/2

