
def test_HeapElement_eq():
    bar = _HeapElement(1.1, "a")
    foo = _HeapElement(1, "a")
    assert foo == bar
    assert bar == foo
    assert foo == "a"

