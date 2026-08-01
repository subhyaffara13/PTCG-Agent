
def test_instance_new():
    instance = m.NoConstructorNew()  # .__new__(m.NoConstructor.__class__)
    cstats = ConstructorStats.get(m.NoConstructorNew)
    assert cstats.alive() == 1
    del instance
    assert cstats.alive() == 0

