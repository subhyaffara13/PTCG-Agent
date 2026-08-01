
def test_cyclic_gc():
    # One object references itself
    instance = m.DynamicClass()
    instance.circular_reference = instance

    cstats = ConstructorStats.get(m.DynamicClass)
    assert cstats.alive() == 1
    del instance
    assert cstats.alive() == 0

    # Two object reference each other
    i1 = m.DynamicClass()
    i2 = m.DynamicClass()
    i1.cycle = i2
    i2.cycle = i1

    assert cstats.alive() == 2
    del i1, i2
    assert cstats.alive() == 0

