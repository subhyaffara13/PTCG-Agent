
def test_issue_13792():
    i =  integrate(log(1/x) / (1 - x), (x, 0, 1))
    assert not i.has(Integral)

