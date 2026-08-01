
def test_unique_deleter():
    m.MyObject4a(0)
    o = m.MyObject4b(23)
    assert o.value == 23
    cstats4a = ConstructorStats.get(m.MyObject4a)
    assert cstats4a.alive() == 2
    cstats4b = ConstructorStats.get(m.MyObject4b)
    assert cstats4b.alive() == 1
    del o
    assert cstats4a.alive() == 1  # Should now only be one leftover
    assert cstats4b.alive() == 0  # Should be deleted
    m.MyObject4a.cleanup_all_instances()
    assert cstats4a.alive() == 0
    assert cstats4b.alive() == 0

