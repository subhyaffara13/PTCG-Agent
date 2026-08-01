
def test_set(capture, doc):
    s = m.get_set()
    assert isinstance(s, set)
    assert s == {"key1", "key2", "key3"}

    s.add("key4")
    with capture:
        m.print_anyset(s)
    assert (
        capture.unordered
        == """
        key: key1
        key: key2
        key: key3
        key: key4
    """
    )

    m.set_add(s, "key5")
    assert m.anyset_size(s) == 5

    m.set_clear(s)
    assert m.anyset_empty(s)

    assert not m.anyset_contains(set(), 42)
    assert m.anyset_contains({42}, 42)
    assert m.anyset_contains({"foo"}, "foo")

    assert doc(m.get_set) == "get_set() -> set"
    assert doc(m.print_anyset) == "print_anyset(arg0: anyset) -> None"


def test_set(doc):
    """std::set <-> set"""
    s = m.cast_set()
    assert s == {"key1", "key2"}
    s.add("key3")
    assert m.load_set(s)
    assert m.load_set(frozenset(s))

    assert doc(m.cast_set) == "cast_set() -> Set[str]"
    assert doc(m.load_set) == "load_set(arg0: Set[str]) -> bool"


def test_set():
    from sympy.abc import x, y
    s = set()
    assert srepr(s) == "set()"
    s = {x, y}
    assert srepr(s) in ("{Symbol('x'), Symbol('y')}", "{Symbol('y'), Symbol('x')}")


def test_set():
    assert sstr(set()) == 'set()'
    assert sstr(frozenset()) == 'frozenset()'

    assert sstr({1}) == '{1}'
    assert sstr(frozenset([1])) == 'frozenset({1})'
    assert sstr({1, 2, 3}) == '{1, 2, 3}'
    assert sstr(frozenset([1, 2, 3])) == 'frozenset({1, 2, 3})'

    assert sstr(
        {1, x, x**2, x**3, x**4}) == '{1, x, x**2, x**3, x**4}'
    assert sstr(
        frozenset([1, x, x**2, x**3, x**4])) == 'frozenset({1, x, x**2, x**3, x**4})'

