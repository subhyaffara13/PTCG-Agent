
def test_issue_22982_15323():
    assert limit((log(E + 1/x) - 1)**(1 - sqrt(E + 1/x)), x, oo) == oo
    assert limit((1 - 1/x)**x*(log(1 - 1/x) + 1/(x*(1 - 1/x))), x, 1, dir='+') == 1
    assert limit((log(E + 1/x) )**(1 - sqrt(E + 1/x)), x, oo) == 1
    assert limit((log(E + 1/x) - 1)**(- sqrt(E + 1/x)), x, oo) == oo

