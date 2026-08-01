
def test_wild_matchpy():
    from sympy.utilities.matchpy_connector import WildDot, WildPlus, WildStar

    matchpy = import_module("matchpy")

    if matchpy is None:
        return

    wd = WildDot('w_')
    wp = WildPlus('w__')
    ws = WildStar('w___')

    assert str(wd) == 'w_'
    assert str(wp) == 'w__'
    assert str(ws) == 'w___'

    assert str(wp/ws + 2**wd) == '2**w_ + w__/w___'
    assert str(sin(wd)*cos(wp)*sqrt(ws)) == 'sqrt(w___)*sin(w_)*cos(w__)'

