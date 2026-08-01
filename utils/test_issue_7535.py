
def test_issue_7535():
    assert limit(tan(x)/sin(tan(x)), x, pi/2) == Limit(tan(x)/sin(tan(x)), x, pi/2, dir='+')
    assert limit(tan(x)/sin(tan(x)), x, pi/2, dir='-') == Limit(tan(x)/sin(tan(x)), x, pi/2, dir='-')
    assert limit(tan(x)/sin(tan(x)), x, pi/2, dir='+-') == Limit(tan(x)/sin(tan(x)), x, pi/2, dir='+-')
    assert limit(sin(tan(x)),x,pi/2) == AccumBounds(-1, 1)
    assert -oo*(1/sin(-oo)) == AccumBounds(-oo, oo)
    assert oo*(1/sin(oo)) == AccumBounds(-oo, oo)
    assert oo*(1/sin(-oo)) == AccumBounds(-oo, oo)
    assert -oo*(1/sin(oo)) == AccumBounds(-oo, oo)

