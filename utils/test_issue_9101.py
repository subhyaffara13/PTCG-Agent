
def test_issue_9101():
    assert not integrate(log(x + sqrt(x**2 + y**2 + z**2)), z).has(Integral)

