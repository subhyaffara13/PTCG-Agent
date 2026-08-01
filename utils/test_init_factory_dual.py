
def test_init_factory_dual():
    """Tests init factory functions with dual main/alias factory functions"""
    from pybind11_tests.factory_constructors import TestFactory7

    cstats = [TestFactory7.get_cstats(), TestFactory7.get_alias_cstats()]
    cstats[0].alive()  # force gc
    n_inst = ConstructorStats.detail_reg_inst()

    class PythFactory7(TestFactory7):
        def get(self):
            return 100 + TestFactory7.get(self)

    a1 = TestFactory7(1)
    a2 = PythFactory7(2)
    assert a1.get() == 1
    assert a2.get() == 102
    assert not a1.has_alias()
    assert a2.has_alias()

    b1 = TestFactory7(tag.pointer, 3)
    b2 = PythFactory7(tag.pointer, 4)
    assert b1.get() == 3
    assert b2.get() == 104
    assert not b1.has_alias()
    assert b2.has_alias()

    c1 = TestFactory7(tag.mixed, 5)
    c2 = PythFactory7(tag.mixed, 6)
    assert c1.get() == 5
    assert c2.get() == 106
    assert not c1.has_alias()
    assert c2.has_alias()

    d1 = TestFactory7(tag.base, tag.pointer, 7)
    d2 = PythFactory7(tag.base, tag.pointer, 8)
    assert d1.get() == 7
    assert d2.get() == 108
    assert not d1.has_alias()
    assert d2.has_alias()

    # Both return an alias; the second multiplies the value by 10:
    e1 = TestFactory7(tag.alias, tag.pointer, 9)
    e2 = PythFactory7(tag.alias, tag.pointer, 10)
    assert e1.get() == 9
    assert e2.get() == 200
    assert e1.has_alias()
    assert e2.has_alias()

    f1 = TestFactory7(tag.shared_ptr, tag.base, 11)
    f2 = PythFactory7(tag.shared_ptr, tag.base, 12)
    assert f1.get() == 11
    assert f2.get() == 112
    assert not f1.has_alias()
    assert f2.has_alias()

    g1 = TestFactory7(tag.shared_ptr, tag.invalid_base, 13)
    assert g1.get() == 13
    assert not g1.has_alias()
    with pytest.raises(TypeError) as excinfo:
        PythFactory7(tag.shared_ptr, tag.invalid_base, 14)
    assert (
        str(excinfo.value)
        == "pybind11::init(): construction failed: returned holder-wrapped instance is not an "
        "alias instance"
    )

    assert [i.alive() for i in cstats] == [13, 7]
    assert ConstructorStats.detail_reg_inst() == n_inst + 13

    del a1, a2, b1, d1, e1, e2
    assert [i.alive() for i in cstats] == [7, 4]
    assert ConstructorStats.detail_reg_inst() == n_inst + 7
    del b2, c1, c2, d2, f1, f2, g1
    assert [i.alive() for i in cstats] == [0, 0]
    assert ConstructorStats.detail_reg_inst() == n_inst

    assert [i.values() for i in cstats] == [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "100", "11", "12", "13", "14"],
        ["2", "4", "6", "8", "9", "100", "12"],
    ]

