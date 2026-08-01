
def test_stl_ownership():
    cstats = ConstructorStats.get(m.Placeholder)
    assert cstats.alive() == 0
    r = m.test_stl_ownership()
    assert len(r) == 1
    del r
    assert cstats.alive() == 0

