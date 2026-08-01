
def _test_sho1d():
    ad = RaisingOp('a')
    assert pretty(ad) == ' \N{DAGGER}\na '
    assert latex(ad) == 'a^{\\dagger}'

