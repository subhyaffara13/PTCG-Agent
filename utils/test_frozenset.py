
def test_frozenset(capture, doc):
    s = m.get_frozenset()
    assert isinstance(s, frozenset)
    assert s == frozenset({"key1", "key2", "key3"})

    with capture:
        m.print_anyset(s)
    assert (
        capture.unordered
        == """
        key: key1
        key: key2
        key: key3
    """
    )
    assert m.anyset_size(s) == 3
    assert not m.anyset_empty(s)

    assert not m.anyset_contains(frozenset(), 42)
    assert m.anyset_contains(frozenset({42}), 42)
    assert m.anyset_contains(frozenset({"foo"}), "foo")

    assert doc(m.get_frozenset) == "get_frozenset() -> frozenset"

