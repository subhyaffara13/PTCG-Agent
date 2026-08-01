
def test_zeta_series():
    assert zeta(x, a).series(a, z, 2) == \
        zeta(x, z) - x*(a-z)*zeta(x+1, z) + O((a-z)**2, (a, z))

