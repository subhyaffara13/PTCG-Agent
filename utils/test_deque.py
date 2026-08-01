
def test_deque():
    """std::deque <-> list"""
    lst = m.cast_deque()
    assert lst == [1]
    lst.append(2)
    assert m.load_deque(lst)
    assert m.load_deque(tuple(lst))

