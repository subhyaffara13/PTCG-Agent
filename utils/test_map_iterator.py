
def test_map_iterator():
    sm = m.StringMap({"hi": "bye", "black": "white"})
    assert sm["hi"] == "bye"
    assert len(sm) == 2
    assert sm["black"] == "white"

    with pytest.raises(KeyError):
        assert sm["orange"]
    sm["orange"] = "banana"
    assert sm["orange"] == "banana"

    expected = {"hi": "bye", "black": "white", "orange": "banana"}
    for k in sm:
        assert sm[k] == expected[k]
    for k, v in sm.items():
        assert v == expected[k]
    assert list(sm.values()) == [expected[k] for k in sm]

    it = iter(m.StringMap({}))
    for _ in range(3):  # __next__ must continue to raise StopIteration
        with pytest.raises(StopIteration):
            next(it)

