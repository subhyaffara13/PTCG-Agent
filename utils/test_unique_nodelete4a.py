
def test_unique_nodelete4a():
    o = m.MyObject4a(23)
    assert o.value == 23
    cstats = ConstructorStats.get(m.MyObject4a)
    assert cstats.alive() == 1
    del o
    assert cstats.alive() == 1
    m.MyObject4a.cleanup_all_instances()
    assert cstats.alive() == 0

