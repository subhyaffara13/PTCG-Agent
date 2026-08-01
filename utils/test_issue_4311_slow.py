
def test_issue_4311_slow():
    # Not slow when bypassing heurish
    assert not integrate(x*abs(9-x**2), x).has(Integral)

