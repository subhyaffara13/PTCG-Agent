
def test_issue_14811():
    assert limit(((1 + ((S(2)/3)**(x + 1)))**(2**x))/(2**((S(4)/3)**(x - 1))), x, oo) == oo

