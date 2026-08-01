
def test_issue_18473():
    assert limit(sin(x)**(1/x), x, oo) == Limit(sin(x)**(1/x), x, oo, dir='-')
    assert limit(cos(x)**(1/x), x, oo) == Limit(cos(x)**(1/x), x, oo, dir='-')
    assert limit(tan(x)**(1/x), x, oo) == Limit(tan(x)**(1/x), x, oo, dir='-')
    assert limit((cos(x) + 2)**(1/x), x, oo) == 1
    assert limit((sin(x) + 10)**(1/x), x, oo) == 1
    assert limit((cos(x) - 2)**(1/x), x, oo) == Limit((cos(x) - 2)**(1/x), x, oo, dir='-')
    assert limit((cos(x) + 1)**(1/x), x, oo) == AccumBounds(0, 1)
    assert limit((tan(x)**2)**(2/x) , x, oo) == AccumBounds(0, oo)
    assert limit((sin(x)**2)**(1/x), x, oo) == AccumBounds(0, 1)
    # Tests for issue #23751
    assert limit((cos(x) + 1)**(1/x), x, -oo) == AccumBounds(1, oo)
    assert limit((sin(x)**2)**(1/x), x, -oo) == AccumBounds(1, oo)
    assert limit((tan(x)**2)**(2/x) , x, -oo) == AccumBounds(0, oo)


def test_issue_18473():
    assert exp(x*log(cos(1/x))).as_leading_term(x) == S.NaN
    assert exp(x*log(tan(1/x))).as_leading_term(x) == S.NaN
    assert log(cos(1/x)).as_leading_term(x) == S.NaN
    assert log(tan(1/x)).as_leading_term(x) == S.NaN
    assert log(cos(1/x) + 2).as_leading_term(x) == AccumBounds(0, log(3))
    assert exp(x*log(cos(1/x) + 2)).as_leading_term(x) == 1
    assert log(cos(1/x) - 2).as_leading_term(x) == S.NaN
    assert exp(x*log(cos(1/x) - 2)).as_leading_term(x) == S.NaN
    assert log(cos(1/x) + 1).as_leading_term(x) == AccumBounds(-oo, log(2))
    assert exp(x*log(cos(1/x) + 1)).as_leading_term(x) == AccumBounds(0, 1)
    assert log(sin(1/x)**2).as_leading_term(x) == AccumBounds(-oo, 0)
    assert exp(x*log(sin(1/x)**2)).as_leading_term(x) == AccumBounds(0, 1)
    assert log(tan(1/x)**2).as_leading_term(x) == AccumBounds(-oo, oo)
    assert exp(2*x*(log(tan(1/x)**2))).as_leading_term(x) == AccumBounds(0, oo)

