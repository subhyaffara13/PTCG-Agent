
def test_map_delitem():
    mm = m.MapStringDouble()
    mm["a"] = 1
    mm["b"] = 2.5

    assert list(mm) == ["a", "b"]
    assert list(mm.items()) == [("a", 1), ("b", 2.5)]
    del mm["a"]
    assert list(mm) == ["b"]
    assert list(mm.items()) == [("b", 2.5)]

    um = m.UnorderedMapStringDouble()
    um["ua"] = 1.1
    um["ub"] = 2.6

    assert sorted(um) == ["ua", "ub"]
    assert sorted(um.items()) == [("ua", 1.1), ("ub", 2.6)]
    del um["ua"]
    assert sorted(um) == ["ub"]
    assert sorted(um.items()) == [("ub", 2.6)]

