
def test_instance(msg):
    with pytest.raises(TypeError) as excinfo:
        m.NoConstructor()
    assert msg(excinfo.value) == "m.class_.NoConstructor: No constructor defined!"

    instance = m.NoConstructor.new_instance()

    cstats = ConstructorStats.get(m.NoConstructor)
    assert cstats.alive() == 1
    del instance
    assert cstats.alive() == 0

