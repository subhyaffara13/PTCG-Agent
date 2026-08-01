
def test_cpp_iterators():
    assert m.tuple_iterator() == 12
    assert m.dict_iterator() == 305 + 711
    assert m.passed_iterator(iter((-7, 3))) == -4

