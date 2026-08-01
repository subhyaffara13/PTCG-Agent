
def test_issue_23918():
    b = S(2)/3
    assert (b**x).as_base_exp() == (b, x)

