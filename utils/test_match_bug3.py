
def test_match_bug3():
    x, a, b = map(Symbol, 'xab')
    p = Wild('p')
    assert (b*x*exp(a*x)).match(x*exp(p*x)) is None

