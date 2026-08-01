
def test_issue_5843():
    a = 1 + x
    assert (2*a).extract_multiplicatively(a) == 2
    assert (4*a).extract_multiplicatively(2*a) == 2
    assert ((3*a)*(2*a)).extract_multiplicatively(a) == 6*a

