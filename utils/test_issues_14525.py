
def test_issues_14525():
    assert limit(sin(x)**2 - cos(x) + tan(x)*csc(x), x, oo) == AccumBounds(S.NegativeInfinity, S.Infinity)
    assert limit(sin(x)**2 - cos(x) + sin(x)*cot(x), x, oo) == AccumBounds(S.NegativeInfinity, S.Infinity)
    assert limit(cot(x) - tan(x)**2, x, oo) == AccumBounds(S.NegativeInfinity, S.Infinity)
    assert limit(cos(x) - tan(x)**2, x, oo) == AccumBounds(S.NegativeInfinity, S.One)
    assert limit(sin(x) - tan(x)**2, x, oo) == AccumBounds(S.NegativeInfinity, S.One)
    assert limit(cos(x)**2 - tan(x)**2, x, oo) == AccumBounds(S.NegativeInfinity, S.One)
    assert limit(tan(x)**2 + sin(x)**2 - cos(x), x, oo) == AccumBounds(-S.One, S.Infinity)

