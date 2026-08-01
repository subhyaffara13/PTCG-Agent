
def test_map_string_double():
    mm = m.MapStringDouble()
    mm["a"] = 1
    mm["b"] = 2.5

    assert list(mm) == ["a", "b"]
    assert str(mm) == "MapStringDouble{a: 1, b: 2.5}"
    assert "b" in mm
    assert "c" not in mm
    assert 123 not in mm

    # Check that keys, values, items are views, not merely iterable
    keys = mm.keys()
    values = mm.values()
    items = mm.items()
    assert list(keys) == ["a", "b"]
    assert len(keys) == 2
    assert "a" in keys
    assert "c" not in keys
    assert 123 not in keys
    assert list(items) == [("a", 1), ("b", 2.5)]
    assert len(items) == 2
    assert ("b", 2.5) in items
    assert "hello" not in items
    assert ("b", 2.5, None) not in items
    assert list(values) == [1, 2.5]
    assert len(values) == 2
    assert 1 in values
    assert 2 not in values
    # Check that views update when the map is updated
    mm["c"] = -1
    assert list(keys) == ["a", "b", "c"]
    assert list(values) == [1, 2.5, -1]
    assert list(items) == [("a", 1), ("b", 2.5), ("c", -1)]

    um = m.UnorderedMapStringDouble()
    um["ua"] = 1.1
    um["ub"] = 2.6

    assert sorted(um) == ["ua", "ub"]
    assert list(um.keys()) == list(um)
    assert sorted(um.items()) == [("ua", 1.1), ("ub", 2.6)]
    assert list(zip(um.keys(), um.values())) == list(um.items())
    assert "UnorderedMapStringDouble" in str(um)

