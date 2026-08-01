
def test_primezeta():
    mp.dps = 15
    assert primezeta(0.9).ae(1.8388316154446882243 + 3.1415926535897932385j)
    assert primezeta(4).ae(0.076993139764246844943)
    assert primezeta(1) == inf
    assert primezeta(inf) == 0
    assert isnan(primezeta(nan))

