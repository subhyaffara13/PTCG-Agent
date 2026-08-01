
def test_nthroot1():
    q = 1 + sqrt(2) + sqrt(3) + S.One/10**20
    p = expand_multinomial(q**5)
    assert nthroot(p, 5) == q
    q = 1 + sqrt(2) + sqrt(3) + S.One/10**30
    p = expand_multinomial(q**5)
    assert nthroot(p, 5) == q

