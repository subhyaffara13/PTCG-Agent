
def test_HeapElement_getitem():
    foo = _HeapElement(1, "a")
    bar = _HeapElement(1.1, (3, 2, 1))
    assert foo[1] == "a"
    assert foo[0] == 1
    assert bar[0] == 1.1
    assert bar[2] == 2
    assert bar[3] == 1
    pytest.raises(IndexError, bar.__getitem__, 4)
    pytest.raises(IndexError, foo.__getitem__, 2)

