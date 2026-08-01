
def test_nthroot():
    assert nthroot(90 + 34*sqrt(7), 3) == sqrt(7) + 3
    q = 1 + sqrt(2) - 2*sqrt(3) + sqrt(6) + sqrt(7)
    assert nthroot(expand_multinomial(q**3), 3) == q
    assert nthroot(41 + 29*sqrt(2), 5) == 1 + sqrt(2)
    assert nthroot(-41 - 29*sqrt(2), 5) == -1 - sqrt(2)
    expr = 1320*sqrt(10) + 4216 + 2576*sqrt(6) + 1640*sqrt(15)
    assert nthroot(expr, 5) == 1 + sqrt(6) + sqrt(15)
    q = 1 + sqrt(2) + sqrt(3) + sqrt(5)
    assert expand_multinomial(nthroot(expand_multinomial(q**5), 5)) == q
    q = 1 + sqrt(2) + 7*sqrt(6) + 2*sqrt(10)
    assert nthroot(expand_multinomial(q**5), 5, 8) == q
    q = 1 + sqrt(2) - 2*sqrt(3) + 1171*sqrt(6)
    assert nthroot(expand_multinomial(q**3), 3) == q
    assert nthroot(expand_multinomial(q**6), 6) == q

