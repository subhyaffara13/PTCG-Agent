
def test_issue_22863():
    i = integrate((3*x**3-x**2+2*x-4)/sqrt(x**2-3*x+2), (x, 0, 1))
    assert i == -101*sqrt(2)/8 - 135*log(3 - 2*sqrt(2))/16
    assert math.isclose(i.n(), -2.98126694400554)

