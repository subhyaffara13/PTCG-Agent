
def test_issue_4329():
    assert tan(x).series(x, pi/2, n=3).removeO() == \
        -pi/6 + x/3 - 1/(x - pi/2)
    assert cot(x).series(x, pi, n=3).removeO() == \
        -x/3 + pi/3 + 1/(x - pi)
    assert limit(tan(x)**tan(2*x), x, pi/4) == exp(-1)

