
def test_large_holder():
    o = m.MyObject5(5)
    assert o.value == 5
    cstats = ConstructorStats.get(m.MyObject5)
    assert cstats.alive() == 1
    del o
    assert cstats.alive() == 0

