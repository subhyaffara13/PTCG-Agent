
def test_whittaker():
    mp.dps = 15
    assert whitm(2,3,4).ae(49.753745589025246591)
    assert whitw(2,3,4).ae(14.111656223052932215)

