
def test_init_factory_alias():
    """Tests py::init_factory() wrapper with value conversions and alias types"""

    cstats = [m.TestFactory6.get_cstats(), m.TestFactory6.get_alias_cstats()]
    cstats[0].alive()  # force gc
    n_inst = ConstructorStats.detail_reg_inst()

    a = m.TestFactory6(tag.base, 1)
    assert a.get() == 1
    assert not a.has_alias()
    b = m.TestFactory6(tag.alias, "hi there")
    assert b.get() == 8
    assert b.has_alias()
    c = m.TestFactory6(tag.alias, 3)
    assert c.get() == 3
    assert c.has_alias()
    d = m.TestFactory6(tag.alias, tag.pointer, 4)
    assert d.get() == 4
    assert d.has_alias()
    e = m.TestFactory6(tag.base, tag.pointer, 5)
    assert e.get() == 5
    assert not e.has_alias()
    f = m.TestFactory6(tag.base, tag.alias, tag.pointer, 6)
    assert f.get() == 6
    assert f.has_alias()

    assert ConstructorStats.detail_reg_inst() == n_inst + 6
    assert [i.alive() for i in cstats] == [6, 4]

    del a, b, e
    assert [i.alive() for i in cstats] == [3, 3]
    assert ConstructorStats.detail_reg_inst() == n_inst + 3
    del f, c, d
    assert [i.alive() for i in cstats] == [0, 0]
    assert ConstructorStats.detail_reg_inst() == n_inst

    class MyTest(m.TestFactory6):
        def __init__(self, *args):
            m.TestFactory6.__init__(self, *args)

        def get(self):
            return -5 + m.TestFactory6.get(self)

    # Return Class by value, moved into new alias:
    z = MyTest(tag.base, 123)
    assert z.get() == 118
    assert z.has_alias()

    # Return alias by value, moved into new alias:
    y = MyTest(tag.alias, "why hello!")
    assert y.get() == 5
    assert y.has_alias()

    # Return Class by pointer, moved into new alias then original destroyed:
    x = MyTest(tag.base, tag.pointer, 47)
    assert x.get() == 42
    assert x.has_alias()

    assert ConstructorStats.detail_reg_inst() == n_inst + 3
    assert [i.alive() for i in cstats] == [3, 3]
    del x, y, z
    assert [i.alive() for i in cstats] == [0, 0]
    assert ConstructorStats.detail_reg_inst() == n_inst

    assert [i.values() for i in cstats] == [
        ["1", "8", "3", "4", "5", "6", "123", "10", "47"],
        ["hi there", "3", "4", "6", "move", "123", "why hello!", "move", "47"],
    ]

