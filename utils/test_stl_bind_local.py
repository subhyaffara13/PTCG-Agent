
def test_stl_bind_local():
    import pybind11_cross_module_tests as cm

    v1, v2 = m.LocalVec(), cm.LocalVec()
    v1.append(m.LocalType(1))
    v1.append(m.LocalType(2))
    v2.append(cm.LocalType(1))
    v2.append(cm.LocalType(2))

    # Cross module value loading:
    v1.append(cm.LocalType(3))
    v2.append(m.LocalType(3))

    assert [i.get() for i in v1] == [0, 1, 2]
    assert [i.get() for i in v2] == [2, 3, 4]

    v3, v4 = m.NonLocalVec(), cm.NonLocalVec2()
    v3.append(m.NonLocalType(1))
    v3.append(m.NonLocalType(2))
    v4.append(m.NonLocal2(3))
    v4.append(m.NonLocal2(4))

    assert [i.get() for i in v3] == [1, 2]
    assert [i.get() for i in v4] == [13, 14]

    d1, d2 = m.LocalMap(), cm.LocalMap()
    d1["a"] = v1[0]
    d1["b"] = v1[1]
    d2["c"] = v2[0]
    d2["d"] = v2[1]
    assert {i: d1[i].get() for i in d1} == {"a": 0, "b": 1}
    assert {i: d2[i].get() for i in d2} == {"c": 2, "d": 3}

