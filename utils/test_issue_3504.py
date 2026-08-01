
def test_issue_3504():
    a = Symbol("a")
    e = asin(a*x)/x
    assert e.series(x, 4, n=2).removeO() == \
        (x - 4)*(a/(4*sqrt(-16*a**2 + 1)) - asin(4*a)/16) + asin(4*a)/4

