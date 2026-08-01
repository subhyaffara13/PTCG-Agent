
def test_init_factory_casting():
    """Tests py::init_factory() wrapper with various upcasting and downcasting returns"""

    cstats = [
        ConstructorStats.get(c)
        for c in [m.TestFactory3, m.TestFactory4, m.TestFactory5]
    ]
    cstats[0].alive()  # force gc
    n_inst = ConstructorStats.detail_reg_inst()

    # Construction from derived references:
    a = m.TestFactory3(tag.pointer, tag.TF4, 4)
    assert a.value == "4"
    b = m.TestFactory3(tag.shared_ptr, tag.TF4, 5)
    assert b.value == "5"
    c = m.TestFactory3(tag.pointer, tag.TF5, 6)
    assert c.value == "6"
    d = m.TestFactory3(tag.shared_ptr, tag.TF5, 7)
    assert d.value == "7"

    assert ConstructorStats.detail_reg_inst() == n_inst + 4

    # Shared a lambda with TF3:
    e = m.TestFactory4(tag.pointer, tag.TF4, 8)
    assert e.value == "8"

    assert ConstructorStats.detail_reg_inst() == n_inst + 5
    assert [i.alive() for i in cstats] == [5, 3, 2]

    del a
    assert [i.alive() for i in cstats] == [4, 2, 2]
    assert ConstructorStats.detail_reg_inst() == n_inst + 4

    del b, c, e
    assert [i.alive() for i in cstats] == [1, 0, 1]
    assert ConstructorStats.detail_reg_inst() == n_inst + 1

    del d
    assert [i.alive() for i in cstats] == [0, 0, 0]
    assert ConstructorStats.detail_reg_inst() == n_inst

    assert [i.values() for i in cstats] == [
        ["4", "5", "6", "7", "8"],
        ["4", "5", "8"],
        ["6", "7"],
    ]

