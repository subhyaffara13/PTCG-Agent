
def test_rational_independent():
    ri = rational_independent
    assert ri([], x) == []
    assert ri([cos(x), sin(x)], x) == [cos(x), sin(x)]
    assert ri([x**2, sin(x), x*sin(x), x**3], x) == \
        [x**3 + x**2, x*sin(x) + sin(x)]
    assert ri([S.One, x*log(x), log(x), sin(x)/x, cos(x), sin(x), x], x) == \
        [x + 1, x*log(x) + log(x), sin(x)/x + sin(x), cos(x)]

