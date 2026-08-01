
def test_issue_3423():
    x = Symbol("x")
    assert sqrt(x - 1).as_base_exp() == (x - 1, S.Half)
    assert sqrt(x - 1) != I*sqrt(1 - x)

