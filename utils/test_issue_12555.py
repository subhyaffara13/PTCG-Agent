
def test_issue_12555():
    assert limit((3**x + 2* x**10) / (x**10 + exp(x)), x, -oo) == 2
    assert limit((3**x + 2* x**10) / (x**10 + exp(x)), x, oo) is oo

