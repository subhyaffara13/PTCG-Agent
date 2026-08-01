
def test_match_wild_wild():
    p = Wild('p')
    q = Wild('q')
    r = Wild('r')

    assert p.match(q + r) in [ {q: p, r: 0}, {q: 0, r: p} ]
    assert p.match(q*r) in [ {q: p, r: 1}, {q: 1, r: p} ]

    p = Wild('p')
    q = Wild('q', exclude=[p])
    r = Wild('r')

    assert p.match(q + r) == {q: 0, r: p}
    assert p.match(q*r) == {q: 1, r: p}

    p = Wild('p')
    q = Wild('q', exclude=[p])
    r = Wild('r', exclude=[p])

    assert p.match(q + r) is None
    assert p.match(q*r) is None

