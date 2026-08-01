
def test_unique_nodelete():
    o = m.MyObject4(23)
    assert o.value == 23
    cstats = ConstructorStats.get(m.MyObject4)
    assert cstats.alive() == 1
    del o
    assert cstats.alive() == 1
    m.MyObject4.cleanup_all_instances()
    assert cstats.alive() == 0

