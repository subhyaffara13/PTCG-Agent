
def test_mixed_local_global():
    """Local types take precedence over globally registered types: a module with a `module_local`
    type can be registered even if the type is already registered globally.  With the module,
    casting will go to the local type; outside the module casting goes to the global type.
    """
    import pybind11_cross_module_tests as cm

    m.register_mixed_global()
    m.register_mixed_local()

    a = []
    a.append(m.MixedGlobalLocal(1))
    a.append(m.MixedLocalGlobal(2))
    a.append(m.get_mixed_gl(3))
    a.append(m.get_mixed_lg(4))

    assert [x.get() for x in a] == [101, 1002, 103, 1004]

    cm.register_mixed_global_local()
    cm.register_mixed_local_global()
    a.append(m.MixedGlobalLocal(5))
    a.append(m.MixedLocalGlobal(6))
    a.append(cm.MixedGlobalLocal(7))
    a.append(cm.MixedLocalGlobal(8))
    a.append(m.get_mixed_gl(9))
    a.append(m.get_mixed_lg(10))
    a.append(cm.get_mixed_gl(11))
    a.append(cm.get_mixed_lg(12))

    assert [x.get() for x in a] == [
        101,
        1002,
        103,
        1004,
        105,
        1006,
        207,
        2008,
        109,
        1010,
        211,
        2012,
    ]

