
def test_issue_4511():
    # This works, but gives a slightly over-complicated answer.
    f = integrate(cos(x)**2 / (1 - sin(x)), x)
    assert fu(f) == x - cos(x) - 1
    assert f == ((x*tan(x/2)**2 + x - 2)/(tan(x/2)**2 + 1)).expand()

