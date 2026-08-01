
def test_valarray(doc):
    """std::valarray <-> list"""
    lst = m.cast_valarray()
    assert lst == [1, 4, 9]
    assert m.load_valarray(lst)
    assert m.load_valarray(tuple(lst))

    assert doc(m.cast_valarray) == "cast_valarray() -> List[int]"
    assert doc(m.load_valarray) == "load_valarray(arg0: List[int]) -> bool"

